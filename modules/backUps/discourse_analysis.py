import spacy
import re
import string
import networkx as nx
import matplotlib.pyplot as plt
import base64
from io import BytesIO
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

# Función para crear el grafo de resonancia central
def create_central_resonance_graph(doc):
    graph = nx.DiGraph()
    for token in doc:
        if token.is_alpha and not token.is_stop:
            graph.add_node(token.text)
            for child in token.children:
                if child.is_alpha and not child.is_stop:
                    graph.add_edge(token.text, child.text)
    return graph

# Función para dibujar el grafo utilizando Matplotlib
def draw_graph(graph):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(12, 12))
    node_colors = ["blue" if graph.nodes[node].get('label') == 'TOKEN' else "red" for node in graph]
    node_sizes = [100 + 20 * graph.degree(node) for node in graph]
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, node_size=node_sizes, edge_color='gray', font_size=10, font_weight='bold', arrows=True)
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    image_base64 = base64.b64encode(image_png).decode("utf-8")
    return f'<img src="data:image/png;base64,{image_base64}" />'

def procesar_discurso(text):
    cleaned_text = clean_text(text)
    doc = nlp(cleaned_text)
    graph = create_central_resonance_graph(doc)
    graph_image = draw_graph(graph)
    return graph_image
