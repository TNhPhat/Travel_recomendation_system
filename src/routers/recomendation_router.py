from fastapi import APIRouter
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.recomendation_service import recomendation_service
from pydantic import BaseModel

class UserPreference(BaseModel):
    prompt: str
    chosen_tags: list[str]

class GroupRequest(BaseModel):
    users: list[UserPreference]
router = APIRouter()

@router.post('/recomendation/')
def get_group_recommendations(request: GroupRequest):
    data_src = [[user.prompt, user.chosen_tags] for user in request.users]
    recoment_location_id = recomendation_service.get_location_recomendation(data_src)
    return {"recommendations": recoment_location_id}
