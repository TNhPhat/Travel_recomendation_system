import csv
import os
import requests
import json
import sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.geminiAPI_service import geminiAPI_service
from utils.contants import *

GRAPHQL_ENDPOINT = "https://firebasedataconnect.googleapis.com/v1beta/projects/gotogether-e2e22/locations/asia-southeast1/services/gotogether-e2e22-service:executeGraphql"
FIREBASE_TOKEN = os.getenv('FIREBASE_TOKEN')


def send_mutation():
    return 0

def get_tags_list():
    tags = []
    for domain, sub in LOCATION_TAG.items():
        if isinstance(sub, dict):
            for key, lst in sub.items():
                if isinstance(lst, dict):
                    for subkey, sublst in lst.items():
                        tags.extend(sublst)
                else:
                    tags.extend(lst)
        else:
            tags.extend(sub)
    return tags

def get_tag_weight(name,address,description,tags_list_str):
    prompt = f"""
        Bạn là một chuyên gia đánh giá địa điểm du lịch. Dựa vào mô tả sau, hãy đánh trọng số từ 0-1 cho từng tag theo mức độ nổi bật của địa điểm.
            0.0 tới 0.2: ít hoặc không liên quan
            0.2 tới 0.5: liên quan trung bình
            0.5 tới 0.8: liên quan cao
            0.8 tới 1.0: cực kỳ nổi bật, đặc trưng cho địa điểm
        1. Địa điểm:
            Tên: {name}
            Địa chỉ: {address}
            Mô tả: {description}
            Danh sách tag: {tags_list_str}
        2. Trả về kết quả dạng JSON: key là tên tag, value là số thực từ 0-1.
        Ví dụ mẫu đầu ra:
            {{
                "tag_1": 0.1,
                "tag_2": 1.0
            }}
        3. Chỉ trả về các tag có trọng số > 0. Không kèm bất kỳ lời dẫn nào.
        """
    response = geminiAPI_service.send_prompt(prompt)
    clean_text = response.strip("`")  
    clean_text = clean_text.replace("json", "", 1).strip()
    return clean_text

def send_operation(id,label):
    mutation = """
mutation UpdateLocation($locationId: UUID!, $label: String) @auth(level: USER) @transaction {
    location_update(id: $locationId, data: {label: $label})
}
"""
    variables = {
        "locationId": id,
        "label": label
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('FIREBASE_TOKEN')}",
    }

    response = requests.post(
        GRAPHQL_ENDPOINT,
        json={"query": mutation, "variables": variables},
        headers=headers
    )
    print(response.status_code)
    print(response.text)


def run_pineline():
    file_path = "C:\\Users\\Phat Truong\\Documents\\GitHub\\Travel_recomendation_system\\data\\database.csv"
    column_names = ['id', 'address', 'col3', 'description','col5','name','col7','opening_hour','col9','label']
    data = pd.read_csv(file_path, header=None, names=column_names)
    tags_list = get_tags_list()
    tags_list_str = ','.join(f'"{tag}"' for tag in tags_list)
    for index, row in data.iterrows():
        id = row['id']
        name = row['name']
        description = row['description']
        print(f'Processing {name}: {index}/{data.shape[0]}')
        address = row['address']
        tag_dict = json.loads(get_tag_weight(name,address,description,tags_list_str))
        tag_dict_str = str(tag_dict)
        send_operation(id,tag_dict_str)
    
run_pineline()