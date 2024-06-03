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

    for ent in doc.ents:
        graph.add_node(ent.text, label=ent.label_)

    for token in doc:
        if token.ent_type_:
            continue  # Ignorar tokens que son entidades
        for child in token.children:
            if child.ent_type_:
                if not graph.has_node(child.text):
                    graph.add_node(child.text, label=child.ent_type_)
                graph.add_edge(token.text, child.text, dep=child.dep_)
            else:
                if not graph.has_node(child.text):
                    graph.add_node(child.text, label='TOKEN')
                graph.add_edge(token.text, child.text, dep=child.dep_)
    return graph

# Función para dibujar el grafo utilizando Matplotlib
def draw_graph(graph, top_n=10):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(12, 12))

    # Calcular la centralidad de grado
    centrality = nx.degree_centrality(graph)
    # Ordenar los nodos por centralidad y seleccionar los top_n nodos
    top_nodes = sorted(centrality, key=centrality.get, reverse=True)[:top_n]
    subgraph = graph.subgraph(top_nodes)

    node_colors = [get_color(subgraph.nodes[node].get('label', 'TOKEN')) for node in subgraph]
    node_labels = {node: f"{node} ({subgraph.nodes[node].get('label', 'TOKEN')})" for node in subgraph}

    nx.draw(subgraph, pos, with_labels=False, node_color=node_colors, edge_color='gray', node_size=500, font_size=8, font_weight='bold', arrows=True)
    nx.draw_networkx_labels(subgraph, pos, labels=node_labels, font_size=8, horizontalalignment='left')
    edge_labels = nx.get_edge_attributes(subgraph, 'dep')
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels, font_color='red')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    image_base64 = base64.b64encode(image_png).decode('utf-8')

    # Agregar la leyenda en castellano
    legend = """
    <h3>Relaciones de Dependencia:</h3>
    <ul>
        <li><strong>advcl:</strong> cláusula adverbial</li>
        <li><strong>amod:</strong> modificador adjetival</li>
        <li><strong>obj:</strong> objeto</li>
        <li><strong>appos:</strong> aposición</li>
        <li><strong>flat:</strong> aplanar (estructura plana)</li>
    </ul>
    """

    return f'<img src="data:image/png;base64,{image_base64}" /><div>{legend}</div>'

# Función para obtener el color basado en la categoría de la entidad nombrada
def get_color(label):
    colors = {
        'PER': '#ff6d6d',  # Persona
        'ORG': '#ff8686',  # Organización
        'LOC': '#ffa0a0',  # Localización
        'MISC': '#ffb9b9', # Misceláneo
        'DATE': '#ffd3d3', # Fecha
        'TIME': '#cccc00', # Tiempo
        'MONEY': '#006700', # Dinero
        'PERCENT': '#008000', # Porcentaje
        'FAC': '#009a00', # Instalación
        'GPE': '#00b300', # Entidad política
        'LANGUAGE': '#00cd00', # Idioma
        'WORK_OF_ART': '#ffcc99', # Obra de arte
        'EVENT': '#ff9999', # Evento
        'PRODUCT': '#ff66b2', # Producto
        'LAW': '#cc99ff', # Ley
        'NORP': '#6699ff', # Nacionalidad o afiliación religiosa o política
        'QUANTITY': '#66ff99', # Cantidad
        'ORDINAL': '#ff9966', # Ordinal
        'CARDINAL': '#ffcc66', # Cardinal
        'TOKEN': '#6699ff' # Color azul para tokens
    }
    return colors.get(label, '#6699ff')  # Color azul claro para TOKEN

def analisis_semantico(text):
    cleaned_text = clean_text(text)
    doc = nlp(cleaned_text)
    graph = create_semantic_graph(doc)
    graph_image = draw_graph(graph)
    return graph_image

if __name__ == "__main__":
    texto_prueba = """
    Stanza es una biblioteca de procesamiento del lenguaje natural (NLP) desarrollada por Stanford NLP Group, que ofrece una serie de herramientas de análisis lingüístico para muchos idiomas. Sus capacidades se extienden desde la segmentación de texto hasta análisis más complejos como el reconocimiento de partes del discurso, análisis de entidades nombradas, análisis sintáctico y semántico, entre otros.
    """
    graph_image = analisis_semantico(texto_prueba)
    with open("graph_image.html", "w") as file:
        file.write(graph_image)
    print(graph_image)