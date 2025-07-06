from dotenv import load_dotenv
import os
import requests
from typing import List
load_dotenv()
SERPER_API_KEY=os.getenv("SERPER_API_KEY")

class ImageSearchService:
    def __init__(self):
        self.image_search_url="https://google.serper.dev/images"
        self.text_search_url="https://google.serper.dev/search"
        self.headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
    
    def search_images(self, query: str, site:str=None, num:int=5)->List[str]:
        """
        Search for images using Serper API.
        
        :param query: The search query.
        :param site: Optional site to restrict the search to.
        :param num: Number of images to return.
        :return: List of image URLs.
        """
        params = {
            "q": f"site:{site} {query}" if site else query,
            "num": num
        }

        
        response = requests.get(self.image_search_url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return [item["imageUrl"] for item in data.get("images", [])]
        else:
            raise Exception(f"Error fetching images: {response.status_code} - {response.text}")

# Example usage
# image_search_service = ImageSearchService() 
# query="Oversized Denim Layering"
# site="www.whowhatwear.com"
# images = image_search_service.search_images(query, site=site, num=5)
# print(images)