from google.cloud import firestore
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.contants import *
import re
import pandas as pd
from google.cloud import firestore

class FirestoreService:
    def __init__(self):
        self.db = firestore.Client.from_service_account_json("serviceAccountKey.json")
        self.reviews_db = pd.DataFrame(columns=["Id","locationId","sentimentScore"])
    
    def get_locations_dataframe(self):
        column_names = ['id', 'address', 'category', 'description', 'coordinates', 
                       'name', 'city', 'opening_hour', 'province', 'label','sentiment_sum','num_reviews','sentiment_score']
        
        locations_ref = self.db.collection("locations")
        location_docs = locations_ref.stream()
        data = []
        for doc in location_docs:
            location = doc.to_dict()
            row = {
                'id': location.get('id', ''),
                'address': location.get('address', ''),
                'category': location.get('category', ''),
                'description': location.get('description', ''),
                'coordinates': location.get('coordinates', ''),
                'name': location.get('name', ''),
                'city': location.get('city', ''),
                'opening_hour': location.get('opening_hour', ''),
                'province': location.get('provine', ''), 
                'label': location.get('label', ''),
                'sentiment_sum': 0.0,
                'num_reviews': 0,
                'sentiment_score': 0.0
            }
            data.append(row)
        df = pd.DataFrame(data, columns=column_names)
        return df
    
    def listen_reviews_realtime(self,on_update):
        """
        Lắng nghe toàn bộ /reviews tự động cập nhật theo ADD / MODIFY / REMOVE.
        on_update(location_id, sentiment_sum, count) được gọi mỗi khi 1 location thay đổi.
        """

        def apply_change(change):
            doc_id = change.document.id
            data = change.document.to_dict()
            location_id = data["locationId"]

            if change.type.name == "ADDED":
                sentiment = data.get("sentimentScore", 0)
                review = [doc_id,location_id,sentiment]
                self.reviews_db.loc[len(self.reviews_db)] = review
                return location_id

            elif change.type.name == "MODIFIED":
                sentiment = data.get("sentimentScore", 0)
                self.reviews_db.loc[self.reviews_db['Id'] == doc_id, 'sentimentScore'] = sentiment
                return location_id

            elif change.type.name == "REMOVED":
                self.reviews_db = self.reviews_db[self.reviews_db['Id'] != doc_id]
                return location_id

            return None
        
        def recompute(location_id):
            df_loc = self.reviews_db[self.reviews_db["locationId"] == location_id]

            sentiment_sum = float(df_loc["sentimentScore"].sum()) if len(df_loc) > 0 else 0.0
            count = int(len(df_loc))

            on_update(location_id, sentiment_sum, count)

        def on_snapshot(col_snapshot, changes, read_time):
            affected_locations = set()

            for change in changes:
                location_id = apply_change(change)
                if location_id:
                    affected_locations.add(location_id)

            for location_id in affected_locations:
                recompute(location_id)

        return self.db.collection("reviews").on_snapshot(on_snapshot)
    
    
    
firestore_service = FirestoreService()