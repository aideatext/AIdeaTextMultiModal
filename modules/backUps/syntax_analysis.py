import spacy
import spacy_streamlit
from spacy.tokens import Token
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

def generate_displacy_svgs(docs):
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

    svgs = []
    for doc in docs:
        for token in doc:
            token._.color = colors.get(token.pos_, "#000000")

        svg = displacy.render(doc, style='dep', jupyter=False, options=options)
        for token in doc:
            svg = svg.replace(
                f'<text class="token" fill="#000000">{token.text}</text>',
                f'<text class="token" fill="{token._.color}">{token.text}</text>'
            )

        # Minimize the white space
        svg = svg.replace('<svg', '<svg style="margin: 0; padding: 0; background-color: white;"')

        svgs.append(svg)

    return svgs

#def format_svg(svg):
#    return f'''
#    <style>
#    .displacy {
#        display: flex;
#        flex-direction: column;
#        align-items: center;
#        width: 100%;
#    }
#    </style>
#    {svg}
#    '''

def format_svg(svg):
    return f'''
    <style>
    .displacy {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }
    </style>
    {svg}
    '''

def analisis_sintactico(text):
    sentences = [sent.text.strip() for sent in nlp(text).sents]
    docs = [nlp(sentence) for sentence in sentences]
    svgs = generate_displacy_svgs(docs)
    return [format_svg(svg) for svg in svgs]

if __name__ == "__main__":
    # Prueba del análisis sintáctico
    texto_prueba = "Este es un texto de prueba. Aquí hay otra oración."
    print(analisis_sintactico(texto_prueba))