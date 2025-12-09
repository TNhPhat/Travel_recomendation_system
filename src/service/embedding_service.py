import torch
import numpy
from math import *
import torch.nn.functional as F
import numpy as np
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.contants import *
import re

class EmbeddingService:
    def __init__(self):
        self.tag_pos = {tag: pos for pos,tag in enumerate(get_tags_list())}
    
    def embedding(self,tag_dict):
        embedded_list = [0]*len(self.tag_pos)
        for key,val in tag_dict.items():
            embedded_list[self.tag_pos[key]] = val
        return np.array(embedded_list)
    
    def combine_embedding_vector(self,numpy_list):
        return np.mean(numpy_list,axis = 0)
    
    def convert_embedded_to_dict(self,embedded_array):
        tag_dict = {}
        for index,num in enumerate(embedded_array):
            if(num > 0):
                tag_dict.update({tags_list[index]:num})
        return tag_dict

    def calc_cosine(self,vector1,vector2):
        if(vector1.size != vector2.size):
            print("Len Error (cosine)")
            return 
        return (np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2)))

embedding_service = EmbeddingService()



    
