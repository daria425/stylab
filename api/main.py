from app.services.fashion_classifier import FashionClassifier
from app.services.fashion_analyzer import generate_summary, generate_image_prompt
from app.services.scrapers import PinterestScraper
from app.services.fashion_image_gen import create_garment_image, create_3d_render
from app.utils.logger import logger
from app.utils.file_utils import save_to_json
import json
import time
import asyncio
from datetime import datetime
cached_fashion_classification_file_path="output_data/fashion_classification_results.json"

async def main(use_cached_data:bool=False):
    current_year= datetime.now().year
    query=f"street style trends {current_year}"
    logger.info("Fashion classification and trend summary process started.")
    if use_cached_data: 
        with open(cached_fashion_classification_file_path, "r") as file:
            results = json.load(file)
    else: 
        # run full pipeline
        results = []
        scraper= PinterestScraper(query=query, num_scrols=3)
        scraped_data = await scraper.scrape(save_results=True)
        classifier = FashionClassifier()
        for i, d in enumerate(scraped_data):
            image_url = d["img"]
            logger.info(f"Processing image {i+1}/{len(scraped_data)}: {d['title']}")
            result = classifier.process_label_classification(image_url)
            results.append({
                "title": d["title"],
                "url": d["url"],
                "img": d["img"],
                "classification": result
            })
            time.sleep(1)
    save_to_json(results, "fashion_classification_results.json", output_dir="output_data") # return in API call 
    summary= generate_summary(results)
    logger.info("Trend summary generated successfully.")
    prompts_dict=generate_image_prompt(summary)
    prompts= prompts_dict["prompts"]
    for i, prompt in enumerate(prompts):
       file_path=create_garment_image(prompt, i+1)
    #    create_3d_render(file_path, i+1)
    logger.info("Garment images generated successfully.Pipeline completed.")
    
if __name__ == "__main__":
    asyncio.run(main(use_cached_data=False))