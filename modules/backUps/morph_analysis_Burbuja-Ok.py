import requests
import plotly.express as px

LAMBDA_URL = "https://5f6b6akff7.execute-api.us-east-2.amazonaws.com/DEV/morphAnalyzer"

POS_LABELS = {
    'ADP': 'Preposición',
    'DET': 'Determinante',
    'CONJ': 'Conjunción',
    'CCONJ': 'Conjunción Coordinante',
    'SCONJ': 'Conjunción Subordinante',
    'ADJ': 'Adjetivo',
    'ADV': 'Adverbio',
    'NOUN': 'Sustantivo',
    'VERB': 'Verbo',
    'PROPN': 'Nombre Propio',
    'PRON': 'Pronombre',
    'AUX': 'Auxiliar'
}

COLOR_MAP = {
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

def analisis_morfologico(text):
    response = requests.post(LAMBDA_URL, json={"text": text})
    if response.status_code == 200:
        result = response.json()
        word_frequency = result['word_frequency']
        pos_count = result['pos_count']
        most_common_word = result['most_common_word']
        least_common_word = result['least_common_word']
        most_common_word_pos = result['most_common_word_pos']
        least_common_word_pos = result['least_common_word_pos']
        word_count = result['word_count']

        pos_labels = []
        words = []
        frequencies = []
        colors = []

        # Preparar datos para el gráfico
        for pos, count in pos_count.items():
            if pos in ['NUM', 'PUNCT', 'SPACE']:
                continue
            pos_label = POS_LABELS.get(pos, pos)
            pos_labels.append(pos_label)
            pos_words = sorted([(word.split('_')[0], freq) for word, freq in word_frequency.items() if word.split('_')[1] == pos], key=lambda x: x[1], reverse=True)[:10]
            pos_words_formatted = [f"{word} [{freq}]" for word, freq in pos_words]
            words.append('; '.join(pos_words_formatted))
            frequencies.append(count)
            colors.append(COLOR_MAP.get(pos, 'lightblue'))

        # Crear gráfico de burbujas
        fig = px.scatter(
            x=pos_labels,
            y=frequencies,
            size=frequencies,
            color=pos_labels,
            hover_data={'Frecuencia': frequencies, 'Palabras': words},
            labels={"x": "Categoría Gramatical", "y": "Frecuencia"},
            title="Análisis Morfológico - Frecuencia de Categorías Gramaticales"
        )

        # Agregar anotaciones
        fig.update_layout(
            title={
                'text': "Análisis Morfológico - Frecuencia de Categorías Gramaticales",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            annotations=[
                dict(
                    xref='paper',
                    yref='paper',
                    x=0,
                    y=1.15,
                    xanchor='left',
                    yanchor='top',
                    text=f"Cantidad total de palabras: {word_count}    Palabra más usada: {most_common_word} [{word_frequency[most_common_word]}] ({POS_LABELS.get(most_common_word_pos, most_common_word_pos)})    Palabra menos usada: {least_common_word} [{word_frequency[least_common_word]}] ({POS_LABELS.get(least_common_word_pos, least_common_word_pos)})",
                    showarrow=False,
                    font=dict(size=12)
                )
            ],
            legend_title_text='Categorías Gramaticales'
        )

        return fig
    else:
        return f"Error: {response.json().get('error', 'No se pudo realizar el análisis')}"