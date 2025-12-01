from fastapi import APIRouter
import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.service.geminiAPI_service import geminiAPI_service
from pydantic import BaseModel

class location(BaseModel):
    location_name :str
router = APIRouter()

@router.post('/get_location_tag')
def get_location_tag(location):
    return geminiAPI_service.location_tag_extract(location)

@router.post('/get_scripts_tag')
def get_script_tag(script):
    return geminiAPI_service.scripts_tag_extract(script)
 
