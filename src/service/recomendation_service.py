import json
import pandas as pd
import ast
import math
from math import *
import torch.nn.functional as F
import numpy as np
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.contants import *
from service.embedding_service import embedding_service
from service.geminiAPI_service import geminiAPI_service
import re

class RecomendationService:
    def __init__(self):
        column_names = ['id', 'address', 'category', 'description','coordinates','name','city','opening_hour','provine','label','col11']
        self.dataset = pd.read_csv('data\\database.csv',header = None,names=column_names)
        self.dataset['feature'] = [np.array([]) for _ in range(len(self.dataset))]
        self.dataset['max_cosine'] = [0.0 for _ in range(len(self.dataset))]
        for index,row in self.dataset.iterrows():
            self.dataset.at[index, 'feature'] = embedding_service.embedding(ast.literal_eval(row['label']))
        self.dataset.drop(['label','col11'],axis=1,inplace = True)
        self.dataset['sentiment_score'] = [0.0 for _ in range(len(self.dataset))]
        # self.dataset['sentiment_score'] = np.random.uniform(-1, 1, size=len(self.dataset))

    #dict_locaitonId_voteNum {string:int}
    def get_shedule_input_data(self,dict_locaitonId_VoteNum):
        data = []
        for id,voteNum in dict_locaitonId_VoteNum.items():
            info = {}
            locaiton_info = self.dataset.loc[self.dataset['id'] == id].reset_index(drop=True).iloc[0]
            info.update({"id" : id})
            info.update({"name": locaiton_info['name']})
            info.update({"opening hour": locaiton_info['opening_hour']})
            info.update({"coordinates": locaiton_info['coordinates']})
            info.update({"address": locaiton_info['address']})
            info.update({"Votes": voteNum})
            data.append(info)
        return data
    
    def get_schedule(self,dict_locaitonId_VoteNum,time_start,time_end):
        location_data = self.get_shedule_input_data(dict_locaitonId_VoteNum)
        location_data_str = json.dumps(location_data,indent=4,ensure_ascii=False)
        return self.get_schedule_gemini_response(location_data_str,time_start,time_end)


    def get_schedule_gemini_response(self,location_data_string,time_start,time_end):
        #Lưu ý: JSON đầu vào cần có các trường: id, name, coordinates (hoặc khu vực), votes, avg_duration_min, opening_hours.*
        prompt = f"""# VAI TRÒ (ROLE)
        Bạn là một chuyên gia lập lịch trình du lịch (AI Travel Planner) sử dụng thuật toán tối ưu hóa "Orienteering Problem". Mục tiêu của bạn không phải là đi hết tất cả các điểm, mà là tối đa hóa trải nghiệm (dựa trên số Vote) trong khung thời gian cho phép, đảm bảo sức khỏe và tính khả thi về di chuyển.

        # DỮ LIỆU ĐẦU VÀO (INPUT DATA)

        1. **Thông tin chuyến đi:**
        - Thời gian bắt đầu (Start Time) (YYYY-MM-DDTHH:MM:00.000000Z): {time_start}
        - Thời gian kết thúc (End Time) (YYYY-MM-DDTHH:MM:00.000000Z): {time_end}

        2. **Danh sách địa điểm (JSON Pool):**
        (Dưới đây là danh sách các địa điểm tiềm năng. Hãy coi đây là một "kho lựa chọn", KHÔNG phải là danh sách "phải đi hết")(opening hour = 00:00 - 00:00 là mở cả ngày)
        {location_data_string}

        # QUY TẮC XỬ LÝ (STRICT RULES) - PHẢI TUÂN THỦ

        Để tạo ra lịch trình "Hợp lý" (Reasonable Itinerary), bạn phải tuân thủ nghiêm ngặt các logic sau:

        1. **Logic Sàng lọc (Selection based on Score):**
        - Ưu tiên chọn các địa điểm có `votes` cao nhất.
        - Nếu quỹ thời gian không đủ, hãy MẠNH DẠN BỎ QUA (SKIP) các địa điểm có `votes` thấp. Đừng cố nhồi nhét.

        2. **Logic Địa lý & Di chuyển (Geography & Transit):**
        - Nhóm các địa điểm gần nhau (`coordinates`) để đi cùng một buổi. Tránh đi hình ziczac.
        - BẮT BUỘC tính thời gian di chuyển giữa các điểm:
            + 15 phút: Nếu cùng khu vực/quận.
            + 30-45 phút: Nếu khác khu vực.
        - Cộng thêm 10 phút "Buffer Time" (thời gian đệm) sau mỗi lần di chuyển để trừ hao kẹt xe/chờ đợi.

        3. **Logic Thời gian thực (Real-time Constraints):**
        - Kiểm tra kỹ `opening_hours`. Nếu đến nơi mà đóng cửa -> Lịch trình thất bại (Invalid).
        - Nếu lịch trình cần chừa thời gian ăn uống ngủ nghỉ không chèn các hoạt động vào các thời điểm như vậy.

        4. **Logic Trải nghiệm (Pacing):**
        - Không xếp quá 2 địa điểm "nặng đô" (thời gian tham quan > 90 phút) liên tiếp nhau mà không có nghỉ ngơi.

        # ĐỊNH DẠNG ĐẦU RA (OUTPUT FORMAT)

        Chỉ trả về duy nhất một chuỗi JSON (Valid JSON String), không kèm bất kỳ lời dẫn hay markdown nào khác. Cấu trúc JSON như sau:

        {{
        "schedule": [
            "location"{{
                "id": locationid,
                "start_time": "YYYY-MM-DDTHH:MM:00.000000Z",
                "end_time": "YYYY-MM-DDTHH:MM:00.000000Z",
            }}
        ]
        }}"""
        print(prompt)
        response = geminiAPI_service.send_prompt(prompt)
        clean_text = response.strip("`")  
        clean_text = clean_text.replace("json", "", 1).strip()
        print(json.loads(clean_text))
        return json.loads(clean_text)




    def calc_cosine(self,favourite_embedded):
        self.dataset['cosine'] = np.nan
        for index,row in self.dataset.iterrows():
            self.dataset.at[index,'cosine'] = embedding_service.calc_cosine(row['feature'],favourite_embedded)

    def calc_recomnentation_score(self,favourite_embedded):
        self.calc_cosine(favourite_embedded)
        self.dataset['recomendation_score'] = 0.7*self.dataset['cosine'] + 0.3*self.dataset['sentiment_score']

    def get_person_favourite_embedded(self, prompt, list_tags):
        prompt_tag_dict = {}
        if len(prompt) > 0:
            prompt_tag_dict = json.loads(
                geminiAPI_service.get_tag_from_prompt(prompt, get_tags_list())
            )
        chosen_tag_dict = {tag: 1.0 for tag in list_tags}
        prompt_tag_embedded = embedding_service.embedding(prompt_tag_dict)
        chosen_tag_embedded = embedding_service.embedding(chosen_tag_dict)

        rms_weights = np.sqrt((chosen_tag_embedded**2 + prompt_tag_embedded**2) / 2)
        rms_weights = np.where(chosen_tag_embedded == 0, 
                            prompt_tag_embedded, 
                            rms_weights)
        rms_weights = np.where(prompt_tag_embedded == 0, 
                            chosen_tag_embedded, 
                            rms_weights)
        return rms_weights

    
    #data src [[prompt,[list_chosen_tag]]]
    def get_group_favourite_embedded(self,data_src):
        group_favourite_embedded = []
        for user_data in data_src:
            user_prompt = user_data[0]
            user_chosen_tag = user_data[1]
            group_favourite_embedded.append(self.get_person_favourite_embedded(user_prompt,user_chosen_tag))
        return embedding_service.combine_embedding_vector(group_favourite_embedded)
    
    #data src [tag_dict]
    def get_group_favourite_embedded2(self,tag_dict_list):
        group_favourite_embedded = []
        for tag_dict in tag_dict_list:
            group_favourite_embedded.append(embedding_service.embedding(tag_dict))
        return embedding_service.combine_embedding_vector(group_favourite_embedded)
    
    
    def tag_probabilities(self,tag_vector):
        v = np.array(tag_vector, dtype=float)
        v = np.maximum(v, 0)
        s = np.sum(v)
        return v / s if s > 0 else np.zeros_like(v)
    
    def tag_entropy(self,tag_probs):
        eps = 1e-12
        return -np.sum(tag_probs * np.log(tag_probs + eps))
    
    def lambda_from_entropy(self,entropy, n_tag, min_lambda=0.5, max_lambda=1):
        # normalize 0 → 1
        norm = entropy / np.log(n_tag)
        # entropy thấp => λ cao ; entropy cao => λ thấp
        return max_lambda - norm * (max_lambda - min_lambda)

    def mmr_select(self, top_k=10,lambda_param = 0.9):
        # lambda_param = self.auto_lambda(top_k)
        # print(lambda_param)
        print(lambda_param)
        if 'recomendation_score' not in self.dataset.columns:
            raise ValueError("Bạn cần chạy calc_recomnentation_score(favourite_embedded) trước")
        most_recomendation_score = np.argmax(self.dataset['recomendation_score'])
        selected_idxs = [most_recomendation_score]
        candidate_idxs = list(range(len(self.dataset)))
        candidate_idxs.remove(most_recomendation_score)
        embeddings = np.stack(self.dataset['feature'].values)
        scores = self.dataset['recomendation_score'].values

        while len(selected_idxs) < top_k and candidate_idxs:
            mmr_values = []
            for idx in candidate_idxs:
                if not selected_idxs:
                    mmr_val = scores[idx]
                else:
                    sim_to_selected = max([
                        np.dot(embeddings[idx], embeddings[j]) /
                        (np.linalg.norm(embeddings[idx]) * np.linalg.norm(embeddings[j]))
                        for j in selected_idxs
                    ])
                    mmr_val = lambda_param * scores[idx] - (1 - lambda_param) * sim_to_selected
                mmr_values.append(mmr_val)
            
            idx_max = candidate_idxs[np.argmax(mmr_values)]
            selected_idxs.append(idx_max)
            candidate_idxs.remove(idx_max)
        
        return self.dataset.iloc[selected_idxs].reset_index(drop=True)
    

    def get_location_recomendation(self,favourite_vector,number_of_location):
        favourite_embedded = embedding_service.embedding(favourite_vector)
        self.calc_recomnentation_score(favourite_embedded)
        location = self.mmr_select(number_of_location,lambda_param=self.lambda_from_entropy(self.tag_entropy(self.tag_probabilities(favourite_embedded)), len(favourite_embedded)))
        location_id = location['id'].tolist()
        return location_id,location['name'].tolist(),location['cosine'].tolist()

    def get_group_location_recomendation(self,data_src,number_of_location,tag_dict = False):
        if not tag_dict:
            favourite_embedded = self.get_group_favourite_embedded(data_src)
        else:
            favourite_embedded = self.get_group_favourite_embedded2(data_src)
        
        self.calc_recomnentation_score(favourite_embedded)
        location = self.mmr_select(number_of_location,lambda_param=self.lambda_from_entropy(self.tag_entropy(self.tag_probabilities(favourite_embedded)), len(favourite_embedded)))
        location_id = location['id'].tolist()
        return location_id,location['name'].tolist()

recomendation_service = RecomendationService()
#recomendation_service.get_schedule({"c789879d-8538-4c56-8479-87a13a27d704": 3,"2fb7f19e-53b5-4f76-803c-4978c5184cb7": 1,"2508a054-602f-4d40-84a8-68f21cae02f5":5},"2025-12-10T05:00:00.000000Z","2025-12-13T05:00:00.000000Z")




    


    


    
