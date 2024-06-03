import os
import re
import string
import networkx as nx
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import spacy
from spacy.lang.es.stop_words import STOP_WORDS

# Cargar el modelo spaCy localmente
nlp = spacy.load("es_core_news_lg")

# Función para limpiar el texto de entrada
def clean_text(text):
    text = "".join([char.lower() for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)  # Eliminar números
    text = re.sub(' +', ' ', text)  # Eliminar espacios adicionales
    tokens = re.split('\W+', text)  # Tokenizar el texto
    text = [word for word in tokens if word not in STOP_WORDS]  # Eliminar palabras vacías
    cleaned_text = " ".join(text)  # Convertir la lista de tokens de nuevo en una cadena
    return cleaned_text

# Función para crear el grafo semántico
def create_semantic_graph(doc):
    graph = nx.DiGraph()
    for token in doc:
        graph.add_node(token.text, pos=token.pos_)
        for child in token.children:
            graph.add_edge(token.text, child.text, dep=child.dep_)
    return graph

# Función para dibujar el grafo
def draw_graph(graph):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(12, 12))
    node_colors = [get_color(graph.nodes[node]['pos']) for node in graph]
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=3000, font_size=10, font_weight='bold', arrows=True)
    edge_labels = nx.get_edge_attributes(graph, 'dep')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    image_base64 = base64.b64encode(image_png).decode("utf-8")
    return f"data:image/png;base64,{image_base64}"

# Función para obtener el color basado en la categoría gramatical
def get_color(pos):
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
    return colors.get(pos, '#000000')

def analisis_semantico(text):
    cleaned_text = clean_text(text)
    doc = nlp(cleaned_text)
    graph = create_semantic_graph(doc)
    graph_image = draw_graph(graph)

    return graph_image

if __name__ == "__main__":
    texto_prueba = "Este es un texto de prueba para análisis semántico."
    print(analisis_semantico(texto_prueba))
