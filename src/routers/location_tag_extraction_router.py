from fastapi import APIRouter
import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.location_tag_extraction_service import tag_extraction_service
from pydantic import BaseModel

class location(BaseModel):
    location_name :str
router = APIRouter()

@router.post('/get_tag')
def get_tag(location):
    return tag_extraction_service.tag_extract(location)
 
