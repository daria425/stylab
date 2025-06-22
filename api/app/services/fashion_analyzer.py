from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Union, Dict
from app.utils.file_utils import load_txt_instuctions
import json
category_gen_instruction_file_path = "instructions/category_generation_instructions.txt"
trend_summary_instruction_file_path = "instructions/trend_summary_instructions.txt"

client = genai.Client(
    vertexai=True, project="social-style-scan", location="us-central1"
)

class FashionClassificationCategories(BaseModel):
    silhouette: List[str] = Field(
        ..., 
        description="List of keywords describing the silhouette present in the image"
    )
    garments: List[str] = Field(
        ..., 
        description="List of garment categories in the image for fashion classification."
    )
    fabrics: List[str] = Field(
        ..., 
        description="List of fabric types in the image for fashion classification."
    )
    aesthetics: List[str] = Field(
        ..., 
        description="List of aesthetic styles relating to the image for fashion classification."
    )
    accessories: Union[List[str], None] = Field(
        ..., 
        description="A list of keywords describing accessories present in the image if any"
    )
    color_palette: List[str] = Field(
        ..., 
        description="A list of colors present in the image for fashion classification."
    )
    print_or_pattern: Union[List[str], None] = Field(
        ..., 
        description="A list of prints or patterns present in the image for fashion classification."
    )
    styling_details: Union[List[str], None] = Field(
        ..., 
        description="A list of styling details present in the image for fashion classification."
    )

def generate_categories(image_bytes:bytes):
    system_instruction = load_txt_instuctions(category_gen_instruction_file_path)
    contents = [
        {
            "role": "user",
            "parts": [
                {
                    "text": "Generate a list of categories for a detailed description of the provided image."
                },
                {"inlineData": {"mimeType": "image/jpeg", "data": image_bytes}},
            ],
        }
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_schema=FashionClassificationCategories.model_json_schema(),
            response_mime_type="application/json",
        ),
    )
    categories=response.text
    categories_dict = json.loads(categories)
    return categories_dict
    
def generate_summary(trend_dataset: List[Dict[str, Union[str, Dict]]]):
    system_instruction = load_txt_instuctions(trend_summary_instruction_file_path)
    contents = [
    {
        "role": "user",
        "parts": [
            {
                "text": "Here is the dataset. Each entry represents an image scraped from Pinterest, labeled by a zero-shot classifier and visual language model. Please summarize the emerging fashion trends across the full dataset."
            },
            {
                "text": json.dumps(trend_dataset, indent=2)
            }
        ]
    }
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
        ),
    )
    summary = response.text
    return summary

