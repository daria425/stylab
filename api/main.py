from app.services.fashion_classifier import FashionClassifier
from app.services.fashion_analyzer import generate_summary, generate_image_prompt
from app.utils.logger import logger
from typing import List, Dict
import json
import time
scraped_data_file_path="output_data/pinterest_street+style+trends+2025.json"
cached_fashion_classification_file_path="output_data/fashion_classification_results.json"
with open(scraped_data_file_path, "r") as file:
    scraped_data = json.load(file)

def main(scraped_data:List[Dict[str, str]], use_cached_data:bool=False):
    logger.info("Fashion classification and trend summary process started.")
    classifier = FashionClassifier()
    if use_cached_data:
        with open(cached_fashion_classification_file_path, "r") as file:
            results = json.load(file)
    else:
      results = []
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
    summary= generate_summary(results)
    logger.info("Trend summary generated successfully.")
    print(summary)
    prompts=generate_image_prompt(summary)
    print(prompts)
    logger.info("Fashion classification and trend summary process completed.")

if __name__ == "__main__":
    main(scraped_data, use_cached_data=True)
    # Example usage:
    # scraped_data = [
    #     {"title": "Image 1", "url": "http://example.com/image1.jpg", "img": "http://example.com/image1.jpg"},
    #     {"title": "Image 2", "url": "http://example.com/image2.jpg", "img": "http://example.com/image2.jpg"}
    # ]
    # main(scraped_data)