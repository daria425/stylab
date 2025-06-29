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

async def main(use_cached_data:bool=False, save_data:bool=False):
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
    data={
        "trend_analysis": results,
        "images":[]

    }
    if save_data:
        save_to_json(results, "fashion_classification_results.json", output_dir="output_data")
    summary= generate_summary(results)
    data["trend_summary"]=summary
    logger.info("Trend summary generated successfully.")
    prompts_dict=generate_image_prompt(summary)
    prompts= prompts_dict["prompts"]
    for i, prompt in enumerate(prompts):
       image_data_url=create_garment_image(prompt=prompt, image_num=i+1, save_image=True)
       data["images"].append({
              "prompt": prompt,
              "image_data_url": image_data_url
       })
    #    create_3d_render(file_path, i+1)
    logger.info("Garment images generated successfully.Pipeline completed.")
    return data
    
if __name__ == "__main__":
    asyncio.run(main(use_cached_data=False))