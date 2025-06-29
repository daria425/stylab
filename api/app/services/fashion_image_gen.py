from dotenv import load_dotenv
import os
import requests
from app.utils.logger import logger
load_dotenv()
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

def create_garment_image(prompt:str, image_num:int, output_dir:str="generated_images")-> str:
    """
    Create a garment image using Stability AI's image generation API.
    Args:
        prompt (str): The text prompt to guide the image generation.
        image_num (int): The image number for naming the output file.
        output_dir (str): The directory where the generated image will be saved.
    Returns:
        str: The file path of the generated image.
    """
    logger.info(f"Generating image {image_num} with prompt: {prompt}")
    prompt=f"{prompt}. White background, high resolution, photography, soft lighting, studio"
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
            "prompt": prompt, 

        },
    )

    if response.status_code == 200:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        file_path= f"{output_dir}/image_{image_num}.jpg"
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return file_path
    else:
        raise Exception(str(response.json()))

def create_3d_render(file_path:str, image_num:int, output_dir:str="generated_images"):
    response = requests.post(
        f"https://api.stability.ai/v2beta/3d/stable-fast-3d",
        headers={
            "authorization": f"Bearer {STABILITY_API_KEY}",
        },
        files={
            "image": open(file_path, "rb")
        },
        data={},
    )
    three_d_file_path = f"{output_dir}/3d_image_{image_num}.glb"
    if response.status_code == 200:
        with open(three_d_file_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))