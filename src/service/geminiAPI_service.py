from dotenv import load_dotenv
import os
load_dotenv()
import time
import google.generativeai as genai
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.contants import *
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class GeminiAPI_service():
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash") 

    def sleep(self):
        print("sleep for 5 seconds")
        time.sleep(5)

    def get_tag_from_prompt(self,user_prompt,tag_list):
        prompt = f"""
        Bạn là một chuyên gia đánh giá mong muốn du lịch của người dùng. Hãy đọc đoạn mô tả mong muốn đi du lịch người dùng sau và đánh trọng số từ 0 đến 1 cho từng tag có thể áp dụng.
        Thang trọng số (bắt buộc áp dụng chính xác):
            0.90 tới 1.00 → Mong muốn chính (primary intent): Xuất hiện nổi bật, được nhấn mạnh, hoặc là mục tiêu quan trọng nhất.
            0.00 → Trường hợp còn lại
        1. Mong muốn của người dùng : {user_prompt}
        2. Danh sách tag: {','.join([f'"{tag}"' for tag in tag_list])}
        3. Hãy làm nổi bật rõ ràng các mong muốn chính bằng việc gán trọng số cao vượt trội so với các mức còn lại.
        4. Tuyệt đối không để các tag ngoài lề có trọng số cao gây loãng đề xuất (các tag không liên quan hoặc ít nên để trọng số 0.0)
        5. Trả về kết quả dạng JSON: key là tên tag, value là số thực từ 0-1.
        Ví dụ mẫu đầu ra:
            {{
                "tag_1": 0.1,
                "tag_2": 1.0
            }}
        6. Chỉ trả về các tag có trọng số > 0. Không kèm bất kỳ lời dẫn nào.
        """
        response = self.send_prompt(prompt)
        clean_text = response.strip("`")  
        clean_text = clean_text.replace("json", "", 1).strip()
        return clean_text

    def send_prompt(self,prompt):
        response = self.model.generate_content(prompt)
        self.sleep()
        return response.text

geminiAPI_service = GeminiAPI_service()
