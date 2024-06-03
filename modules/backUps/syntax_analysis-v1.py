import requests
import plotly.graph_objects as go
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np

LAMBDA_URL = "https://5f6b6akff7.execute-api.us-east-2.amazonaws.com/DEV/syntaxAnalyzer"

def analisis_sintactico(text):
    response = requests.post(LAMBDA_URL, json={"text": text})
    if response.status_code == 200:
        result = response.json()
        edges = result['edges']

        # Preparar datos para el dendograma
        labels = list(set([edge['source'] for edge in edges] + [edge['target'] for edge in edges]))
        distances = np.ones((len(labels), len(labels)))

        for edge in edges:
            source_idx = labels.index(edge['source'])
            target_idx = labels.index(edge['target'])
            distances[source_idx][target_idx] = 0
            distances[target_idx][source_idx] = 0

        linked = linkage(distances, 'single')

        fig = go.Figure()

        dendro = dendrogram(linked, labels=labels, orientation='left', no_plot=True)

        for i in range(len(dendro['icoord'])):
            xi = dendro['icoord'][i]
            yi = dendro['dcoord'][i]
            fig.add_trace(go.Scatter(x=yi, y=xi, mode='lines', line_color='black'))

        fig.update_layout(
            title="Análisis Sintáctico - Dendograma de Dependencias",
            xaxis_title="Palabras",
            yaxis_title="Relaciones"
        )

        return fig
    else:
        return f"Error: {response.json().get('error', 'No se pudo realizar el análisis')}"
