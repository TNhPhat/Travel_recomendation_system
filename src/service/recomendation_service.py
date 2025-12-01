import json
import pandas as pd
import ast
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
        column_names = ['id', 'address', 'col3', 'description','col5','name','col7','opening_hour','col9','label','col11']
        self.dataset = pd.read_csv('data\\database.csv',header = None,names=column_names)
        self.dataset['feature'] = [np.array([]) for _ in range(len(self.dataset))]
        self.dataset['max_cosine'] = [0.0 for _ in range(len(self.dataset))]
        for index,row in self.dataset.iterrows():
            self.dataset.at[index, 'feature'] = embedding_service.embedding(ast.literal_eval(row['label']))
        self.dataset.drop(['label','col11'],axis=1,inplace = True)
        self.dataset['sentiment_score'] = [0.0 for _ in range(len(self.dataset))]
        self.dataset['sentiment_score'] = np.random.uniform(-1, 1, size=len(self.dataset))

    def calc_cosine(self,favourite_embedded):
        self.dataset['cosine'] = np.nan
        for index,row in self.dataset.iterrows():
            self.dataset.at[index,'cosine'] = embedding_service.calc_cosine(row['feature'],favourite_embedded)

    def calc_recomnentation_score(self,favourite_embedded):
        self.calc_cosine(favourite_embedded)
        self.dataset['recomendation_score'] = 0.7*self.dataset['cosine'] + 0.3*self.dataset['sentiment_score']

    def get_person_favourite_embedded(self,prompt,list_tags):
        prompt_tag_dict = {}
        if(len(prompt) > 0):
            prompt_tag_dict = json.loads(geminiAPI_service.get_tag_from_prompt(prompt,get_tags_list()))
        chosen_tag_dict = {tag:0.6 for tag in list_tags}
        prompt_tag_embedded = embedding_service.embedding(prompt_tag_dict)
        chosen_tag_embedded = embedding_service.embedding(chosen_tag_dict)
        rms_weights = np.sqrt((chosen_tag_embedded**2 + prompt_tag_embedded**2) / 2)
        return rms_weights
    
    #data src [[prompt,[list_chosen_tag]]]
    def get_group_favourite_embedded(self,data_src):
        group_favourite_embedded = []
        for user_data in data_src:
            user_prompt = user_data[0]
            user_chosen_tag = user_data[1]
            group_favourite_embedded.append(self.get_person_favourite_embedded(user_prompt,user_chosen_tag))
        return embedding_service.combine_embedding_vector(group_favourite_embedded)
    
    def mmr_select(self, top_k=20, lambda_param=0.7):
        if 'recomendation_score' not in self.dataset.columns:
            raise ValueError("Bạn cần chạy calc_recomnentation_score(favourite_embedded) trước")
        selected_idxs = []
        candidate_idxs = list(range(len(self.dataset)))
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
    
    def get_location_recomendation(self,data_src):
        favourite_embedded = self.get_group_favourite_embedded(data_src)
        self.calc_recomnentation_score(favourite_embedded)
        location = self.mmr_select()
        location_id = location['id'].tolist()
        return location_id

recomendation_service = RecomendationService()




    


    


    
