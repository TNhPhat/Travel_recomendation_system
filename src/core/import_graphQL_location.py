import csv
import os
import requests
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from service.geminiAPI_service import geminiAPI_service

GRAPHQL_ENDPOINT = "https://firebasedataconnect.googleapis.com/v1beta/projects/gotogether-e2e22/locations/asia-southeast1/services/gotogether-e2e22-service:executeGraphql"
def predict_label(name, address):
    try:
        labels = geminiAPI_service.location_tag_extract(name)
        return labels if isinstance(labels, list) else []
    except Exception as e:
        print("Gemini error:", e)
        return []

def get_coordinates(address):
    if not address:
        return None
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": "AIzaSyAaIcYNJ-MZuCnp8p36j51j18VF7o_gu0M"}
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
      $label: [String!]
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
        "gps": get_coordinates(row["address"]),
        "category": row["main_category"],
        "description": geminiAPI_service.get_decription(row["name"],row["address"]),
        "hours": geminiAPI_service.get_opening_hours(row["name"],row["address"]),
        "province": "Bà Rịa - Vũng Tàu",
        "city": "Bà Rịa - Vũng Tàu",
        "label": row.get("label"),
    }
    # print(variables)
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



def run_pipeline():
    file_path = "data/all-task-11-overview.csv"

    rows = []
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Loaded {len(rows)} records")

    # 2. Auto label + Insert to DataConnect
    for idx, row in enumerate(rows):
        print(f"\n[{idx+1}/{len(rows)}] Processing {row['name']}")

        # Auto-label
        labels = predict_label(row["name"], row["address"])
        row["label"] = labels

        # Push to Firebase DataConnect
        result = send_mutation(row)
        print(result)

