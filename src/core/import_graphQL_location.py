import csv
import os
import requests
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.geminiAPI_service import geminiAPI_service
from utils.contants import *

GRAPHQL_ENDPOINT = "https://firebasedataconnect.googleapis.com/v1beta/projects/gotogether-e2e22/locations/asia-southeast1/services/gotogether-e2e22-service:executeGraphql"


def get_opening_hour(name,address):
    prompt = f"""
    1. Bạn hãy tìm nguồn về địa điểm {name} ở địa chỉ {address} và lấy giờ hoạt động trong 1 ngày (chỉ tìm giờ không có thứ, ngày nghỉ,...).
    2. Nếu không tìm thấy nguồn về địa điểm hãy cho 1 giờ hoạt động hợp lí.
    2. Định dạng đầu ra là HH:MM - HH:MM (ví dụ 7:00 - 10:00). Nếu mở 24/7 thì đưa ra 00:00 - 00:00
    3. Chỉ đưa ra giờ hoạt động đúng định dạng không kèm bất kì lời dẫn nào thêm.
    """
    response = geminiAPI_service.send_prompt(prompt)
    return response


def get_tag_weight(name,address,tags_list_str):
    prompt = f"""
        Bạn là một chuyên gia đánh giá địa điểm du lịch. Dựa vào mô tả sau, hãy đánh trọng số từ 0-1 cho từng tag theo mức độ nổi bật của địa điểm.
        Thang trọng số (bắt buộc):
            0.85 tới 1.00 → Hoàn toàn phù hợp (đặc trưng chính của địa điểm). Ví dụ: “Bãi biển Hồ Cốc” → tag “biển” = 1.0.
            0.45 tới 0.65 → Phù hợp trung bình, đặc trưng phụ nhưng có liên quan rõ ràng. Ví dụ: “Nhà hàng hải sản gần biển” → tag “biển” = 0.55
            0.10 tới 0.35 → Phù hợp nhẹ hoặc chỉ liên quan gián tiếp. Ví dụ: “Café ven biển” → tag “cà phê” = 0.3, “biển” = 0.2.
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
    
def get_description(name,address):
    prompt = f"""
    Hãy tìm kiếm thông tin đáng tin cậy trên Internet về địa điểm dưới đây, sau đó đọc và tổng hợp nội dung từ các nguồn đó để viết một mô tả chính xác, ngắn gọn và không bịa đặt.
    Tên địa điểm: {name}
    Địa chỉ: {address}

    Quy tắc quan trọng:

        1. Chỉ sử dụng thông tin tìm thấy từ các nguồn mà bạn vừa truy cập.

        2. Tuyệt đối không bịa đặt bất kỳ chi tiết nào không xuất hiện trong nguồn.

        3. Nếu thông tin trên Internet không đủ hoặc quá ít, hãy ghi rõ điều đó và chỉ mô tả những gì có thật.

        4. Ưu tiên thông tin từ website chính thức, bản đồ, bài review uy tín, báo, cơ quan du lịch.

        5. Tóm tắt khách quan, không quảng cáo, không thổi phồng. 

        6. Chỉ trả về đầu ra là câu mô tả không bao gồm bất kì lời dẫn nào đi kèm.
    """
    response = geminiAPI_service.send_prompt(prompt)
    return response

def get_coordinates(name,address):
    if not address:
        return None
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"name": name ,"address": address, "key": os.getenv('GOOGLE_MAPS_KEY')}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("status") == "OK" and len(data.get("results", [])) > 0:
            loc = data["results"][0]["geometry"]["location"]
            return f"{loc['lat']},{loc['lng']}"
        else:
            print("Google Maps error:", data.get("status"))
            return None
    except Exception as e:
        print("Error fetching coordinates:", e)
    return None

def send_mutation(row):
    mutation = """
    mutation AddLocation(
      $name: String!,
      $address: String!,
      $gps: String!,
      $category: String!,
      $description: String,
      $hours: String,
      $province: String,
      $city: String,
      $label: String
    ) {
      location_insert(
        data:{
            name: $name,
            address: $address,
            gpsCoordinates: $gps,
            category: $category,
            description: $description,
            openingHours: $hours,
            province: $province,
            city: $city,
            label: $label
        }  
      ) }
    """

    variables = {
        "name": row["name"],
        "address": row["address"],
        "gps": get_coordinates(row['name'],row["address"]),
        "category": row["main_category"],
        "description": row['description'],
        "hours": get_opening_hour(row['name'],row['address']),
        "province": "Thành phố Hồ Chí Minh",
        "city": "Thành phố Hồ Chí Minh",
        "label": row.get("label"),
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



def send_del_mutation(id):
    mutation = """
   mutation DeleteLocation($locationId: UUID!) @auth(level: USER) @transaction {
        location_delete(key: {id: $locationId})
    }
    """
    variables = {
        'locationId': id
    }
    print(variables)
    # headers = {
    #     "Content-Type": "application/json",
    #     "Authorization": f"Bearer {os.getenv('FIREBASE_TOKEN')}",
    # }

    # response = requests.post(
    #     GRAPHQL_ENDPOINT,
    #     json={"query": mutation, "variables": variables},
    #     headers=headers
    # )

    # print(response.status_code)
    # print(response.text)

def run_pipeline():
    
    file_path = "data\\cf_HCM.csv"

    rows = []
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Loaded {len(rows)} records")

    for idx, row in enumerate(rows):
        print(f"\n[{idx+1}/{len(rows)}] Processing {row['name']}")


        row['description'] = get_description(row['name'],row["address"])
        labels = get_tag_weight(row["name"], row["address"],get_tags_list())
        row["label"] = labels

        result = send_mutation(row)
        print(result)


run_pipeline()
# send_del_mutation('d5e879d494a44208b007458b856548d1')

