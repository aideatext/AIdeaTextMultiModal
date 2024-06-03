import os
import requests
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Accede al token de autorización desde las variables de entorno
API_URL = "https://api-inference.huggingface.co/models/spacy/es_core_news_lg"
API_TOKEN = os.getenv("HF_API_TOKEN")
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    print("Status Code:", response.status_code)  # Depuración
    print("Headers:", response.headers)  # Depuración
    print("API Response:", response.text)  # Depuración
    return response.json()

def analyze_text(text):
    return query({"inputs": text})

if __name__ == "__main__":
    response = analyze_text("Este es un texto de prueba.")
    print(response)
