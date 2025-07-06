from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.services.trend_analysis import TrendAnalysisService, get_trend_analysis_service_with_saving
from app.services.fashion_classifier import FashionClassifier
from app.services.scrapers import get_default_pinterest_scraper
from app.models.trend_analysis import TrendAnalysisResponse
from datetime import datetime

origins=["http://localhost:3000", "http://localhost:3001", "https://social-style-scan.vercel.app"]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return RedirectResponse(url="/api/health")
@app.get("/api/health")
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok", "message": "API is running"}
@app.get("/api/trend-analysis", response_model=TrendAnalysisResponse)
async def get_trend_analysis(trend_analysis_service: TrendAnalysisService = Depends(get_trend_analysis_service_with_saving), fashion_classifier: FashionClassifier = Depends(FashionClassifier)):
    """
    Endpoint to trigger the trend analysis service.
    """
    current_year= datetime.now().year
    query=f"street style trends {current_year}"
    pinterest_scraper = get_default_pinterest_scraper(query=query, num_scrols=3)
    result = await trend_analysis_service.run(pinterest_scraper=pinterest_scraper, fashion_classifier=fashion_classifier)
    return result
