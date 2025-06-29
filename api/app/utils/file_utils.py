from PIL import Image
import requests
from pathlib import Path
from io import BytesIO
import os
import json
def fetch_image(url: str, convert_rgb:bool=False) -> tuple[Image.Image, bytes]:
    response = requests.get(url)
    image_bytes = response.content
    img = Image.open(BytesIO(image_bytes))
    if convert_rgb:
        img = img.convert("RGB")
    return img, image_bytes

def load_txt_instuctions(file_path: str) -> str:
    """
    Load instructions from a text file.
    
    :param file_path: Path to the text file containing instructions.
    :return: Content of the text file as a string.
    """
    CONFIG_DIR=Path("app/config")
    file_path = CONFIG_DIR / file_path
    try:
        with open(file_path, 'r') as file:
            instructions = file.read()
        return instructions
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")
    
def save_to_json(data:dict, file_name:str, output_dir:str="output_data"):
    """
    Save data to a JSON file.
    
    :param data: Data to be saved.
    :param file_name: Name of the output JSON file.
    :param output_dir: Directory where the JSON file will be saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = Path(output_dir) / file_name
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {output_path}")