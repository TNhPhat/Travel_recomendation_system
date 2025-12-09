from fastapi import APIRouter
import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.recomendation_service import recomendation_service
from pydantic import BaseModel
from typing import Dict,List

class UserPreference1(BaseModel):
    prompt: str
    chosen_tags: list[str]
class GroupRequest1(BaseModel):
    users: list[UserPreference1]
    number_of_places: int

class DictList(BaseModel):
    tag_dict_list: List[Dict[str, float]]
    number_of_places:int 

class Request3(BaseModel):
    tag_dict: Dict[str, float]
    number_of_places:int 

class schedule_request(BaseModel):
    VoteList: Dict[str,int]
    start_time: str
    end_time: str

router = APIRouter()

@router.post('/group_recomendation_by_user_data')
def get_group_recommendations_by_user_data(request: GroupRequest1):
    data_src = [[user.prompt, user.chosen_tags] for user in request.users]
    recoment_location_id,location_name = recomendation_service.get_group_location_recomendation(data_src,request.number_of_places)
    return {"recommendations": recoment_location_id}

@router.post('/group_recomendation_by_tag_dict')
def get_group_recommendations_by_tag_dict(request: DictList):
    recoment_location_id,location_name = recomendation_service.get_group_location_recomendation(request.tag_dict_list,request.number_of_places,tag_dict=True)
    return {"recommendations": recoment_location_id}

@router.post('/personal_recomendation_by_tag_dict')
def get_personal_recommendations(request: Request3):
    recoment_location_id,location_name,location_cosine = recomendation_service.get_location_recomendation(request.tag_dict,request.number_of_places)
    return {"recommendations": recoment_location_id,"match_score": location_cosine}

@router.post('/get_schedule')
def get_schedule(request: schedule_request):
    schedule = recomendation_service.get_schedule(request.VoteList,request.start_time,request.end_time)
    return schedule


# @router.post('/personal_recomendation_by_user_reference')
# def get_group_recommendations_by_user_data(request: user):
#     data_src = [[user.prompt, user.chosen_tags] for user in request.users]
#     recoment_location_id,location_name = recomendation_service.get_group_location_recomendation(data_src,request.number_of_places)
#     return {"recommendations": recoment_location_id}