import torch
import numpy
import torch.nn.functional as F
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from utils.contants import *

class SentimentService:
    def __init__(self):
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        self.tokenizer = AutoTokenizer.from_pretrained('5CD-AI/Vietnamese-Sentiment-visobert')
        self.device = torch.device("cpu" if not torch.cuda.is_available() else "cuda")
        self.model.to(self.device)


    def analysis(self,text: str):
        input = self.tokenizer(text, padding = True,truncation = True,max_length = 128, return_tensors = "pt").to(self.device)
        output = self.model(**input)
        logits = output.logits
        probabilities = F.softmax(logits,dim = 1)
        probabilities = probabilities.detach().cpu().numpy()
        sentiment_score = 0
        for label,score in enumerate(probabilities[0]):
            sentiment_score = sentiment_score + score*SENTIMENT_LABEL_PARAMETER[label]
        return sentiment_score

sentiment_service = SentimentService()

