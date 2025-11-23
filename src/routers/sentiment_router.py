from fastapi import APIRouter
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.sentiment_service import sentiment_service
from pydantic import BaseModel

class review(BaseModel):
    text :str
router = APIRouter()

@router.post('/analyze')
def analyze_sentiment(review):
    score = sentiment_service.analysis(review)
    return {"sentiment_score": float(score)}
