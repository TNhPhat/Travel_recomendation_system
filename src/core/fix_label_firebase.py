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

def get_tag_weight(name,address,tags_list_str):
    prompt = f"""
        Bạn là một chuyên gia đánh giá địa điểm du lịch. Dựa vào mô tả sau, hãy đánh trọng số từ 0-1 cho từng tag theo mức độ nổi bật của địa điểm.
        Thang trọng số (bắt buộc):
            0.85 tới 1.00 → Hoàn toàn phù hợp (đặc trưng chính của địa điểm). Ví dụ: “Bãi biển Hồ Cốc” → tag “biển” = 1.0.
            0.10 tới 0.35 → Phù hợp nhẹ hoặc chỉ liên quan gián tiếp. Ví dụ: “Café ven biển” → “biển” = 0.2."cà phê"= 1.0.
            0.00 → Không liên quan. Giữ mức thấp để không ảnh hưởng đến hệ thống đề xuất.
        Yêu cầu quan trọng:
            Tìm kiếm trên các nguồn uy tín về thông tin địa điểm để đánh trọng số 1 cách chính xác nhất.
            Nếu địa điểm không nhắc gì liên quan, gán weight = 0.00.
            Tuyệt đối không để các tag “ngoài lề” có trọng số cao.
        1. Địa điểm:
            Tên: {name}
            Địa chỉ: {address}
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
    tag_dict = json.loads(clean_text)
    return str(tag_dict)

def send_operation(id,label):
    mutation = """
mutation UpdateLocation($locationId: UUID!, $label: String,$description: String) @auth(level: USER) @transaction {
    location_update(id: $locationId, data: {label: $label})
}
"""
    variables = {
        "locationId": id,
        "label": label
    }
    #print(variables)
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
    file_path = "data\\database.csv"
    column_names = ['id', 'address', 'col3', 'description','col5','name','col7','opening_hour','col9','label','col11']
    data = pd.read_csv(file_path, header=None, names=column_names)
    tags_list = get_tags_list()
    tags_list_str = ','.join(f'"{tag}"' for tag in tags_list)
    for index, row in data.iterrows():
        id = row['id']
        name = row['name']
        print(f'Processing {name}: {index}/{data.shape[0]}')
        address = row['address']
        tag_dict = get_tag_weight(name,address,get_tags_list())
        tag_dict_str = str(tag_dict)
        send_operation(id,tag_dict_str)
    
run_pineline()