import asyncio
from playwright.async_api import async_playwright
import json
from urllib.parse import quote_plus
from datetime import datetime
from app.utils.logger import logger
from abc import ABC, abstractmethod




class BaseScraper(ABC):
    def __init__(self, query: str, num_scrols: int = 3):
        self.query = quote_plus(query)
        self.num_scrols = num_scrols
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"

    @abstractmethod
    async def scrape(self, save_results:bool=False):
        """
        Abstract method to be implemented by subclasses for scraping logic.
        """
        pass

    async def create_browser_context(self):
        playwright_client= await async_playwright().start()
        browser=await playwright_client.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-web-security"],
        )
        context=await browser.new_context(
            user_agent=self.user_agent,
            viewport={"width": 1280, "height": 800},
        )
        page=await context.new_page()
        return playwright_client, browser, context, page
    
    async def cleanup_browser_context(self, playwright_client, browser, context):
        try:
            if context:
                await context.close()
            if browser:
                await browser.close()
            if playwright_client:
                await playwright_client.stop()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
class PinterestScraper(BaseScraper):

    async def scrape_pins(self, query:str, num_scrols:int=3):
        encoded_query = quote_plus(query)
        search_url = f"https://www.pinterest.com/search/pins/?q={encoded_query}&rs=typed"
        scraped_data = []
        playwright_client=None
        browser=None
        context=None
        page=None
        async with async_playwright() as p:
            playwright_client, browser, context, page = await self.create_browser_context()
            await page.goto(search_url)
            await asyncio.sleep(5)
            try:
                #find the pins on the page
                for _ in range(num_scrols):
                    #scroll down the page
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await asyncio.sleep(2)
                pins = await page.query_selector_all("div[data-test-id='pinWrapper']")
                logger.info(f"Found {len(pins)} pins for query: {query}")

                for i, pin in enumerate(pins):
                    try:
                        title_link=await pin.query_selector("a")
                        if not title_link:
                            continue
                        title=await title_link.get_attribute("aria-label")
                        pin_url=await title_link.get_attribute("href")
                        img=await title_link.query_selector("img")
                        if not img:
                            continue
                        img_src = await img.get_attribute("src")
                        if img_src:
                            extracted_data = {
                                "title": title,
                                "url": pin_url,
                                "img": img_src
                            }
                            scraped_data.append(extracted_data)
                    except Exception as e:
                        logger.error(f"Error processing pin {i}: {e}")
                        continue
            except Exception as e:
                logger.error(f"Error during scraping: {e}")
            finally:
                await self.cleanup_browser_context(playwright_client, browser, context)
                logger.info("Browser context cleaned up successfully.")
        return scraped_data

    
    async def scrape(self, save_results: bool = False):
        logger.info(f"Starting Pinterest scrape for query: {self.query}")
        scraped_data = await self.scrape_pins(self.query, self.num_scrols)
        if save_results:
            with open(f"pinterest_{self.query}.json", "w") as f:
                json.dump(scraped_data, f, indent=2)
            logger.info(f"Results saved to pinterest_{self.query}.json")
        else:
            logger.info("Results not saved, only scraped data returned.")
        logger.info(f"Scraped {len(scraped_data)} pins for query: {self.query}")
        return scraped_data

# Example usage:
# current_year=datetime.now().year
# query=f"street style trends {current_year}"
# scraper = PinterestScraper(query=query, num_scrols=3)
# async def main():
#     results = await scraper.scrape(save_results=True)
#     print(json.dumps(results, indent=2))

# asyncio.run(main())