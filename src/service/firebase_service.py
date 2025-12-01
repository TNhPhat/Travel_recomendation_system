import firebase_admin
from firebase_admin import credentials, firestore
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.service.geminiAPI_service import tag_extraction_service

cred = credentials.Certificate("gotogether-e2e22-firebase-adminsdk-fbsvc-8297e38f4d.json")
firebase_admin.initialize_app(cred)

class FirebaseService:
    def __init__(self):
        cred = credentials.Certificate("gotogether-e2e22-firebase-adminsdk-fbsvc-8297e38f4d.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    
    def fill_empty_tag_locaiton(self,locaiton): 
        locaiton_ref = self.db.collection('Location')
        docs = locaiton_ref.stream()

        count = 0
        for doc in docs:
            data = doc.to_dict().copy()
            if not data['label']:
                tags = tag_extraction_service.location_tag_extract(data['name'] + '. địa chỉ:' + data['address'])
                locaiton_ref.document(doc.id).set({"label":tags})
                count+=1
        
        return (f"{count} locaitons have been fill tags")
    

        

        
