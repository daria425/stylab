from PIL import Image
import requests
from io import BytesIO
def fetch_image(url: str, convert_rgb:bool=False) -> Image.Image:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    if convert_rgb:
        img = img.convert("RGB")
    return img