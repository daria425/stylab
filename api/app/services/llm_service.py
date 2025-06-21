from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
import os
from dotenv import load_dotenv
from app.utils.file_utils import load_txt_instuctions
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

category_gen_instruction_file_path="app/config/instructions/category_generation_instructions.txt"
client= OpenAI(api_key=OPENAI_API_KEY)

class FashionClassificationCategories(BaseModel):
    garments: List[str] = Field(
..., description="List of garment categories in the image for fashion classification.", 
    )
    fabrics: List[str] = Field(
        ..., description="List of fabric types in the image for fashion classification."
    )
    aesthetics: List[str] = Field(
        ..., description="List of aesthetic styles relating to the image for fashion classification."
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
                    "text": f"Generate a list of categories for a detailed description of the provided image. The categories should include garments, fabrics, and aesthetics."
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
    print(response)


img_url="https://i.pinimg.com/236x/91/cd/df/91cddf7888d9151ddcbc0435da0de97e.jpg"
generate_categories(img_url)