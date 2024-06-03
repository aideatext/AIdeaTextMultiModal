import spacy
from spacy.tokens import doc
from spacy import displacy

# Cargar el modelo spaCy localmente
nlp = spacy.load("es_core_news_lg")

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

    for token in doc:
        token._.color = colors.get(token.pos_, "#000000")

    svg = displacy.render(doc, style='dep', jupyter=False, options=options)
    for token in doc:
        svg = svg.replace(f'<text class="token" fill="#000000">{token.text}</text>', f'<text class="token" fill="{token._.color}">{token.text}</text>')

    return svg

def analisis_sintactico(text):
    doc = nlp(text)
    svg = generate_displacy_svg(doc)
    return f'<div style="width: 100%; height: 100%; overflow: auto;">{svg}</div>'
