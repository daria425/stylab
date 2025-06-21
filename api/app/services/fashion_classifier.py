
from transformers import CLIPProcessor, CLIPModel
import torch
sample_data={
    "title": "Sacai Spring 2025 Menswear Fashion Show | Vogue Street Casual, Summer 2025 Runway, Denim Street Style 2025, Denim Spring Summer 2025, Denim Spring 2025, Sacai Spring 2023 Ready To Wear, Sacai Runway, Jeans Trend, Trendy Fall Fashion",
    "url": "/pin/3729612256806176/",
    "img": "https://i.pinimg.com/236x/91/cd/df/91cddf7888d9151ddcbc0435da0de97e.jpg"
  }

label_dictionary = {
  "garment_types": [
    "blouse",
    "crop top",
    "trench coat",
    "pleated skirt",
    "cargo pants",
    "oversized blazer",
    "maxi dress",
    "bomber jacket",
    "tulle skirt",
    "sweater vest"
  ],
  "fabrics": [
    "lace",
    "denim",
    "leather",
    "sheer fabric",
    "cotton",
    "satin",
    "knitwear",
    "tweed",
    "mesh",
    "silk"
  ],
  "aesthetics": [
    "coquette",
    "minimalist",
    "grunge",
    "y2k",
    "old money",
    "gothic",
    "romantic",
    "balletcore",
    "streetwear",
    "avant-garde"
  ]
}


class FashionClassifier:
    def __init__(self, model_name="patrickjohncyh/fashion-clip"):
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model = CLIPModel.from_pretrained(model_name)

    def classify_fashion_image(self, image, labels):
        inputs = self.processor(images=[image], return_tensors="pt", text=labels, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits_per_image = outputs.logits_per_image  # Image-text similarity scores
            probs = logits_per_image.softmax(dim=1)
        top_idx = torch.argmax(probs, dim=1).item()
        top_label = labels[top_idx]
        confidence = probs[0, top_idx].item()
        print(f"Label results: {list(zip(labels, probs[0].tolist()))}")
        print(f"Top match: {top_label} ({confidence:.2%} confidence)")
        return top_label, confidence
    
    def process_label_classification(self, image, label_dictionary):
        results = {}
        for category, labels in label_dictionary.items():
            top_label, confidence = self.classify_fashion_image(image, labels)
            results[category] = {
                "top_label": top_label,
                "confidence": confidence
            }
        return results
