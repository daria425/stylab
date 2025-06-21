from PIL import Image
import requests
from pathlib import Path
from io import BytesIO
def fetch_image(url: str, convert_rgb:bool=False) -> Image.Image:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    if convert_rgb:
        img = img.convert("RGB")
    return img

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