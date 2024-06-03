import spacy
from spacy.tokens import Doc, Token
from spacy import displacy

# Cargar el modelo spaCy localmente
nlp = spacy.load("es_core_news_lg")

# Registrar la extensión 'color' en los tokens
if not Token.has_extension("color"):
    Token.set_extension("color", default="#000000")

# Definir colores para las categorías gramaticales
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

# Definir traducciones para las relaciones de dependencia
dep_labels = {
    'nmod': 'modificador nominal',
    'case': 'caso',
    'conj': 'conjunción',
    'cc': 'coordinación',
    'acl': 'cláusula adjetiva',
    'det': 'determinante',
    'punct': 'puntuación',
    'nsubj': 'sujeto nominal',
    'aux': 'auxiliar',
    'iobj': 'objeto indirecto',
    'xcomp': 'complemento abierto'
}

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

    for token in doc:
        token._.color = colors.get(token.pos_, "#000000")

    svg = displacy.render(doc, style='dep', jupyter=False, options=options)

    for token in doc:
        svg = svg.replace(
            f'<text class="token" fill="#000000">{token.text}</text>',
            f'<text class="token" fill="{token._.color}">{token.text}</text>'
        )

    # Agregar la leyenda de las relaciones de dependencia
    legend = "<div style='margin-top: 20px;'>"
    legend += "<h3>Relaciones de Dependencia:</h3><ul>"
    for dep, translation in dep_labels.items():
        legend += f"<li><strong>{dep}</strong>: {translation}</li>"
    legend += "</ul></div>"

    svg += legend

    # Guardar el SVG en un archivo para depuración
    with open("output.svg", "w", encoding="utf-8") as f:
        f.write(svg)

    return svg

def analisis_sintactico(text):
    doc = nlp(text)
    svg = generate_displacy_svg(doc)

    return f'<div style="width: 100%; height: 100%; overflow: auto;">{svg}</div>'

if __name__ == "__main__":
    # Prueba del análisis sintáctico
    texto_prueba = "Este es un texto de prueba."
    print(analisis_sintactico(texto_prueba))
