import requests
import plotly.express as px

LAMBDA_URL = "https://5f6b6akff7.execute-api.us-east-2.amazonaws.com/DEV/morphAnalyzer"

def analisis_morfologico(text):
    response = requests.post(LAMBDA_URL, json={"text": text})
    if response.status_code == 200:
        result = response.json()
        word_frequency = result['word_frequency']
        pos_count = result['pos_count']
        most_common_word = result['most_common_word']
        least_common_word = result['least_common_word']

        words = list(word_frequency.keys())
        frequencies = list(word_frequency.values())

        fig = px.scatter(
            x=words,
            y=frequencies,
            size=frequencies,
            color=words,
            labels={"x": "Words", "y": "Frequency"},
            title="Análisis Morfológico - Frecuencia de Palabras"
        )
        fig.add_annotation(
            text=f"Most common word: {most_common_word}, Least common word: {least_common_word}",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.1,
            xanchor='center',
            yanchor='bottom'
        )
        return fig
    else:
        return f"Error: {response.json().get('error', 'No se pudo realizar el análisis')}"
