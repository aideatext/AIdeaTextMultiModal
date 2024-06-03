import os
import requests
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Accede al token de autorización desde las variables de entorno
#API_URL = "https://api-inference.huggingface.co/models/spacy/es_core_news_lg"
#API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased
API_URL = "https://api-inference.huggingface.co/models/bert-base-multilingual-cased"

API_TOKEN = os.getenv("HF_API_TOKEN")
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Esto arrojará una excepción si la respuesta HTTP es un error
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    else:
        print("Status Code:", response.status_code)  # Depuración
        print("Headers:", response.headers)  # Depuración
        print("API Response:", response.text)  # Depuración
        return response.json()


def analyze_text(text):
    payload = {
        "inputs": {
            "text": text
        }
    }
    return query(payload)

if __name__ == "__main__":
    #response = analyze_text("Este es un texto de prueba.")
    response = analyze_text("This is a test text.")
    print(response)