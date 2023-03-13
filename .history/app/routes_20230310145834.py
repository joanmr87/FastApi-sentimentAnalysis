from fastapi import APIRouter
from app.services import sentiment_analysis
router = APIRouter()


@router.post("/")
def analyze_sentiment(fromTimestamp: str, toTimestamp: str, email: str):
    print(fromTimestamp)
    print(toTimestamp)
    print(email)
    return "llego el post"
#sentiment_analysis(fromTimestamp, toTimestamp, email)
