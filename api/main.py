from app.services.fashion_classifier import FashionClassifier
from app.services.llm_service import get_trend_summary
from app.utils.logger import logger
import time
from typing import List, Dict
import json
scraped_data_file_path="output_data/pinterest_street+style+trends+2025.json"
with open(scraped_data_file_path, "r") as file:
    scraped_data = json.load(file)

def main(scraped_data:List[Dict[str, str]]):
    logger.info("Fashion classification and trend summary process started.")
    classifier = FashionClassifier()
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
      time.sleep(1)  # Sleep to avoid rate limiting or overloading the API
    summary= get_trend_summary(results)
    logger.info("Trend summary generated successfully.")
    print(summary)
    logger.info("Fashion classification and trend summary process completed.")

if __name__ == "__main__":
    main(scraped_data)
    # Example usage:
    # scraped_data = [
    #     {"title": "Image 1", "url": "http://example.com/image1.jpg", "img": "http://example.com/image1.jpg"},
    #     {"title": "Image 2", "url": "http://example.com/image2.jpg", "img": "http://example.com/image2.jpg"}
    # ]
    # main(scraped_data)