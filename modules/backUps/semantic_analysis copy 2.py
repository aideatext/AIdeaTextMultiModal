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
    for token in doc:
        graph.add_node(token.text, pos=token.pos_)
        for child in token.children:
            graph.add_edge(token.text, child.text, dep=child.dep_)
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
        node_text.append(node)
        node_color.append(get_color(graph.nodes[node]['pos']))

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
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[ dict(
                            text="Análisis Semántico",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002 ) ],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    return fig

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
    graph_figure = draw_graph(graph)

    return graph_figure

if __name__ == "__main__":
    texto_prueba = "Este es un texto de prueba para análisis semántico."
    fig = analisis_semantico(texto_prueba)
    fig.show()
