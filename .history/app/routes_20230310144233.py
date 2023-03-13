from fastapi import APIRouter
from app.services import sentiment_analysis
router = APIRouter()

@router.post("/")
def analyze_sentiment(fromTimestamp: str, toTimestamp: str, email: str):
    return sentiment_analysis(fromTimestamp, toTimestamp, email)
