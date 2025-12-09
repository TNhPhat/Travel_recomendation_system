from fastapi import APIRouter
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.embedding_service import embedding_service
from service.recomendation_service import recomendation_service
from pydantic import BaseModel

class UserPreference(BaseModel):
    prompt: str
    chosen_tags: list[str]

router = APIRouter()

@router.post("/tag_extraction")
def get_tag_dict(request: UserPreference):
    tag_dict = embedding_service.convert_embedded_to_dict(recomendation_service.get_person_favourite_embedded(request.prompt,request.chosen_tags))
    print(tag_dict)
    return {"tag" : tag_dict}
