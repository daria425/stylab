from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Union, Dict
import os
import json
from dotenv import load_dotenv
from app.utils.file_utils import load_txt_instuctions
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

category_gen_instruction_file_path="instructions/category_generation_instructions.txt"
trend_summary_instruction_file_path="instructions/trend_summary_instructions.txt"
client= OpenAI(api_key=OPENAI_API_KEY)

class FashionClassificationCategories(BaseModel):
    silhouette: List[str] = Field(
        ..., 
        description="List of keywords describing the silhouette present in the image", 
        examples=["fitted", "oversized", "boxy", "slim-cut", "a-line", "bodycon", "flared", "tailored"]
    )
    garments: List[str] = Field(
..., description="List of garment categories in the image for fashion classification.", 
    )
    fabrics: List[str] = Field(
        ..., description="List of fabric types in the image for fashion classification."
    )
    aesthetics: List[str] = Field(
        ..., description="List of aesthetic styles relating to the image for fashion classification."
    )
    accessories: Union[List[str], None] = Field(
        ..., 
        description="A list of keywords describing accessories present in the image if any", 
        examples=["silver necklace",
    "leather belt",
    "silk scarf",
    "platinum watch",
    "diamond ring",
    "pearl earrings",
    "suede gloves",
    "chunky bracelet",
    "cashmere shawl",
    "tote bag",
    "oversized sunglasses",
    "wide-brim hat",
    "vintage brooch",
    "floral hair clip",
    "leather wallet",
    "beaded clutch",
    "fur stole",
    "canvas backpack",]
    )
    color_palette: List[str]= Field(
        ..., 
        description="A list of colors present in the image for fashion classification.", 
        examples=[    "monochrome",
    "pastel",
    "vibrant",
    "earthy",
    "neon",
    "muted",
    "bold",
    "subtle",
    "rich",
    "warm",
    "cool",
    "neutral",
    "metallic",
    "dark",
    "light",
    "soft"]
    )
    print_or_pattern:Union[List[str], None] = Field(
        ..., 
        description="A list of prints or patterns present in the image for fashion classification.", 
        examples=["floral", "striped", "polka dot", "plaid", "paisley", "animal print", "geometric", "abstract", "tie-dye", "camouflage"]
    )
    styling_details: Union[List[str], None] = Field(
        ..., 
        description="A list of styling details present in the image for fashion classification.", 
        examples=["layered", "asymmetrical", "pleated", "ruffled", "embroidered", "cropped", "high-waisted", "oversized sleeves", "cut-out", "peplum"]
    )




def generate_categories(image_url:str):
    system_instruction = load_txt_instuctions(category_gen_instruction_file_path)
    input=[
        {
            "role":"developer", 
            "content": system_instruction
        }, 
        {
            "role":"user", 
            "content":[
                {
                    "type": "input_text",
                    "text": f"Generate a list of categories for a detailed description of the provided image. "
                }, 
                {
                    "type": "input_image",
                    "image_url": image_url
                }
            ]
        }

    ]
    schema = FashionClassificationCategories.model_json_schema()
    schema["additionalProperties"] = False  # Ensure no additional properties are allowed
    response=client.responses.create(
        model="gpt-4o", 
        input=input,
        text={
            "format":{
                "type":"json_schema",  
                "name": "fashion_classification_categories",
                "schema": schema}
        }
    )
    output_text=response.output_text
    json_output=json.loads(output_text)
    return json_output


# Example usage:
# image_url="https://i.pinimg.com/236x/91/cd/df/91cddf7888d9151ddcbc0435da0de97e.jpg"
# categories= generate_categories(image_url)
# print(categories)

def get_trend_summary(dataset: List[Dict]):
    system_instruction = load_txt_instuctions(trend_summary_instruction_file_path)
    input=[
        {
            "role":"developer", 
            "content": system_instruction
        }, 
        {
  "role": "user",
  "content": f"Here is the dataset. Each entry represents an image scraped from Pinterest, labeled by a zero-shot classifier and visual language model. Please summarize the emerging fashion trends across the full dataset.{json.dumps(dataset, indent=2)}"
}

    ]
    response=client.responses.create(
        model="gpt-4o", 
        input=input,
      
    )
    return response.output_text

