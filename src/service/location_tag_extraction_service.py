from dotenv import load_dotenv
import os
load_dotenv()
import google.generativeai as genai
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.contants import *
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class TagExtractionService():
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash") 

    def prompt(self,location_name:str):
        prompt = f""" 
1. Cung cấp Địa điểm: {location_name}
2. Cung cấp Danh sách Tag: {", ".join(LOCATION_TAG)}
3. Yêu cầu: Phân tích địa điểm trên và CHỈ chọn tối đa 5 tag và tối thiểu 1 tag phù hợp nhất từ danh sách trên."
4. Đầu ra 1 list tên các tag cách nhau bởi dấu ','.
MẪU ĐẦU RA (Không chứa gì khác):
núi,leo,cửa hàng"""
        return prompt
        
    def tag_extract(self,location_name:str):
        response = self.model.generate_content(self.prompt(location_name)).text
        tags = response.strip().split(',')
        tags_list = [s.strip() for s in tags]
        return tags_list

tag_extraction_service = TagExtractionService()
