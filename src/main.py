import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import FastAPI
# from .routers.sentiment_router import router as sentiment_router
# from .routers.tag_extraction_router import router as tag_extraction_router
from .routers.recomendation_router import router as recomendation_router
app = FastAPI(
    title="Travel Recommendation API",
    version="1.0.0"
)

# app.include_router(sentiment_router, prefix="/sentiment", tags=["sentiment"])
# app.include_router(tag_extraction_router, prefix="/tag_extraction", tags=["tag_extraction"])
app.include_router(recomendation_router, prefix="/location_recomendation", tags=["location_recomendation"])
