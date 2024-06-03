import os
import requests
import plotly.express as px

# Accede al token de autorización desde las variables de entorno
API_URL = "https://api-inference.huggingface.co/models/spacy/es_core_news_lg"
API_TOKEN = os.getenv("HF_API_TOKEN")
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def analyze_text(text):
    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json().get('error', 'No se pudo realizar el análisis')}

def analisis_morfologico(text):
    result = analyze_text(text)
    if "error" in result:
        return f"Error: {result['error']}"

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
