from fastapi import APIRouter
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.sentiment_service import sentiment_service
from pydantic import BaseModel

router = APIRouter()
class SentimentRequest(BaseModel):
    text: str
@router.post('/analyze')
def analyze_sentiment(text: SentimentRequest):
    score = sentiment_service.analysis(text.text)
    return {"sentiment_score": float(score)}
