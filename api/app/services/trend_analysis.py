from app.services.fashion_classifier import FashionClassifier
from app.services.image_search import ImageSearchService
from app.services.fashion_analyzer import generate_summary, generate_image_prompt, get_trend_name
from app.services.scrapers import PinterestScraper
from app.services.fashion_image_gen import create_garment_image, create_3d_render
from app.utils.logger import logger
from app.utils.file_utils import save_to_json, fetch_image
import json
import time
cached_fashion_classification_file_path="output_data/fashion_classification_results.json"



class TrendAnalysisService:
    def __init__(self, use_cached_data: bool = False, save_data: bool = False):
        self.use_cached_data = use_cached_data
        self.save_data = save_data

    async def run(self, pinterest_scraper: PinterestScraper, fashion_classifier: FashionClassifier,image_search_service: ImageSearchService):
        logger.info("Fashion classification and trend summary process started.")
        if self.use_cached_data: 
            with open(cached_fashion_classification_file_path, "r") as file:
                results = json.load(file)
        else: 
            # run full pipeline
            results = []
            scraped_data = await pinterest_scraper.scrape(save_results=self.save_data)
            for i, d in enumerate(scraped_data):
                image_url = d["img"]
                logger.info(f"Processing image {i+1}/{len(scraped_data)}: {d['title']}")
                image, image_bytes = fetch_image(image_url, convert_rgb=True)
                result = fashion_classifier.process_label_classification(image, image_bytes)
                trend_name=get_trend_name(classification_dataset=result, image_bytes=image_bytes)
                trend_images=image_search_service.search_images(trend_name, site="www.whowhatwear.com", num=3)
                results.append({
                    "title": trend_name, 
                    "url": d["url"],
                    "images": trend_images+ [image_url],  
                    "classification": result
                })
                time.sleep(1)
        data={
            "trend_analysis": results,
            "generated_images":[]

        }
        if self.save_data:
            save_to_json(results, "fashion_classification_results.json", output_dir="output_data")
        summary= generate_summary(results)
        data["trend_summary"]=summary
        logger.info("Trend summary generated successfully.")
        prompts_dict=generate_image_prompt(summary)
        prompts= prompts_dict["prompts"]
        for i, prompt in enumerate(prompts):
            image_data_url=create_garment_image(prompt=prompt, image_num=i+1, save_image=self.save_data)
            data["generated_images"].append({
                    "prompt": prompt,
                    "image_data_url": image_data_url
            })
        #    create_3d_render(file_path, i+1)
        logger.info("Garment images generated successfully.Pipeline completed.")
        if self.save_data:
            save_to_json(data, "trend_analysis_results.json", output_dir="output_data")
        else:
            logger.info("Results not saved, only returned.")
        return data

def get_trend_analysis_service_with_saving():
    """
    Factory function to create a TrendAnalysisService instance with saving enabled.
    
    :return: An instance of TrendAnalysisService with saving enabled.
    """
    return TrendAnalysisService(use_cached_data=False, save_data=True)