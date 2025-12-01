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
    
    def calc_cosine(self,vector1,vector2):
        if(vector1.size != vector2.size):
            print("Len Error (cosine)")
            return 
        dot_product = 0
        len_product1 = 0
        len_product2= 0
        for i in range(0,len(vector1)):
            dot_product = dot_product +  vector1[i]*vector2[i]
            len_product1 = len_product1 + vector1[i]**2
            len_product2 = len_product2 + vector2[i]**2
        return (dot_product/(sqrt(len_product1)*sqrt(len_product2)))

embedding_service = EmbeddingService()



    
