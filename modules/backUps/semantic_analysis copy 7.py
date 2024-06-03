import os
import re
import string
import networkx as nx
import plotly.graph_objects as go
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
        for token in ent:
            for child in token.children:
                if child.ent_type_:
                    graph.add_node(child.text, label=child.ent_type_)
                    graph.add_edge(ent.text, child.text, dep=child.dep_)
                else:
                    graph.add_node(child.text, label='TOKEN')
                    graph.add_edge(ent.text, child.text, dep=child.dep_)
    return graph

# Función para dibujar el grafo utilizando Plotly
def draw_graph(graph):
    pos = nx.spring_layout(graph)
    edge_x = []
    edge_y = []

    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    node_color = []

    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_label = graph.nodes[node].get('label', 'TOKEN')
        node_text.append(f"{node} ({node_label})")
        node_color.append(get_color(node_label))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            color=node_color,
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>Red Semántica',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Análisis Semántico",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    return fig

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
        'CARDINAL': '#ffcc66' # Cardinal
    }
    return colors.get(label, '#000000')

def analisis_semantico(text):
    cleaned_text = clean_text(text)
    doc = nlp(cleaned_text)
    graph = create_semantic_graph(doc)
    graph_figure = draw_graph(graph)

    return graph_figure

if __name__ == "__main__":
    texto_prueba = """
    Stanza es una biblioteca de procesamiento del lenguaje natural (NLP) desarrollada por Stanford NLP Group, que ofrece una serie de herramientas de análisis lingüístico para muchos idiomas. Sus capacidades se extienden desde la segmentación de texto hasta análisis más complejos como el reconocimiento de partes del discurso, análisis de entidades nombradas, análisis sintáctico y semántico, entre otros.
    """
    fig = analisis_semantico(texto_prueba)
    fig.show()