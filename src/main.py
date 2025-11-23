import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import FastAPI
from .routers.sentiment_router import router as sentiment_router
from .routers.location_tag_extraction_router import router as tag_extraction_router

app = FastAPI(
    title="Travel Recommendation API",
    version="1.0.0"
)
app.include_router(sentiment_router, prefix="/sentiment", tags=["sentiment"])
app.include_router(tag_extraction_router, prefix="/tag_extraction", tags=["tag_extraction"])
