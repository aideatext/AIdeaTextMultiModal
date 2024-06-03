import os
import requests

# Accede al token de autorización desde las variables de entorno
API_URL = "https://api-inference.huggingface.co/models/spacy/es_core_news_lg"
API_TOKEN = os.getenv("HF_API_TOKEN")
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def analyze_text(text):
    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    return response.json()

def generate_displacy_svg(doc):
    options = {
        "compact": True,
        "bg": "#ffffff",
        "font": "Arial",
        "distance": 90,
        "collapse_punct": False,
        "collapse_phrases": False,
        "offset_x": 100,
        "arrow_stroke": 2,
        "arrow_width": 8,
    }

    colors = {
        'ADP': '#ff6d6d',
        'DET': '#ff8686',
        'CONJ': '#ffa0a0',
        'CCONJ': '#ffb9b9',
        'SCONJ': '#ffd3d3',
        'ADJ': '#ffd3d3',
        'ADV': '#cccc00',
        'NOUN': '#006700',
        'VERB': '#008000',
        'PROPN': '#009a00',
        'PRON': '#00b300',
        'AUX': '#00cd00'
    }

    for token in doc['tokens']:
        token['color'] = colors.get(token['pos'], "#000000")

    svg = displacy.render(doc, style='dep', jupyter=False, options=options)
    for token in doc['tokens']:
        svg = svg.replace(f'<text class="token" fill="#000000">{token["text"]}</text>', f'<text class="token" fill="{token["color"]}">{token["text"]}</text>')

    return svg

def analisis_sintactico(text):
    result = analyze_text(text)
    if "error" in result:
        return f"Error: {result['error']}"

    # Asumiendo que la API de Hugging Face devuelve un resultado similar a lo que se obtenía desde AWS
    doc = result['tokens']
    svg = generate_displacy_svg(doc)
    return f'<div style="width: 100%; height: 100%; overflow: auto;">{svg}</div>'
