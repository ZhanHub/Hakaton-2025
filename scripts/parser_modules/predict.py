import torch
from transformers import BertTokenizer, BertForSequenceClassification
import torch.nn.functional as F

# Модель мен токенизаторды жүктеу
model = BertForSequenceClassification.from_pretrained('models/saved_model/')
tokenizer = BertTokenizer.from_pretrained('models/saved_model/')

id2label = {
    0: 'Религиозный экстремизм',
    1: 'Политический экстремизм',
    2: 'Ксенофобия',
    3: 'Экстремизм бар'
}

def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
    
    probs = probs[0].cpu().numpy()
    
    result = {}
    for idx, prob in enumerate(probs):
        result[id2label[idx]] = round(prob * 100, 2)
    
    predicted_class = id2label[int(probs.argmax())]
    
    return result, predicted_class
