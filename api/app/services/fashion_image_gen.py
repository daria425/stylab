from dotenv import load_dotenv
import os
import requests
from app.utils.logger import logger
load_dotenv()
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

def create_garment_image(prompt:str, image_num:int):
    logger.info(f"Generating image {image_num} with prompt: {prompt}")
    prompt=f"{prompt}. White background, high resolution, photography"
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
        headers={
            "authorization": f"Bearer {STABILITY_API_KEY}",
            "accept": "image/*"
        },
        files={
"none":""
        },
        
        data={
            "prompt": prompt
        },
    )

    if response.status_code == 200:
        output_dir = "generated_images"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(f"{output_dir}/image_{image_num}.jpg", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
