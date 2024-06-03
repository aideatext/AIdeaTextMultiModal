# hf_api.py

import requests
import os

# Accede al token de autorización desde las variables de entorno
API_URL = "https://api-inference.huggingface.co/models/spacy/es_core_news_lg"
API_TOKEN = os.getenv("HF_API_TOKEN")
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def analyze_text(text):
    return query({"inputs": text})
