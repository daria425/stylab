from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class ClassificationCategory(BaseModel):
    top_label: Optional[str] = Field(None, description="The top classification label")
    confidence: Optional[float] = Field(None, description="Confidence score for the top label")
    label_results: Dict[str, float] = Field(default_factory=dict, description="All classification results with confidence scores")

class TrendAnalysisItem(BaseModel):
    title: str = Field(..., description="Title/description of the fashion item")
    url: str = Field(..., description="URL/path to the original image")
    images: List[str] = Field(default_factory=list, description="List of image URLs related to the trend")
    classification: Dict[str, ClassificationCategory] = Field(..., description="Fashion classification results")

class TrendImage(BaseModel):
    prompt: str = Field(..., description="Text prompt used to generate the image")
    image_data_url: str = Field(..., description="Path or data URL of the generated image")

class TrendAnalysisResponse(BaseModel):
    trend_summary: str = Field(..., description="AI-generated summary of fashion trends")
    generated_images: List[TrendImage] = Field(default_factory=list, description="Generated fashion images")
    trend_analysis: List[TrendAnalysisItem] = Field(default_factory=list, description="Analyzed fashion items from Pinterest")

