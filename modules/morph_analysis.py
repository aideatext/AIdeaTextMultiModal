import spacy
import plotly.express as px

# Cargar el modelo spaCy localmente
nlp = spacy.load("es_core_news_lg")

# Definir etiquetas y colores para las categorías gramaticales
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
    doc = nlp(text)
    word_frequency = {}
    pos_count = {}

    for token in doc:
        pos = token.pos_
        word = token.text.lower()
        word_pos = f"{word}_{pos}"
        word_frequency[word_pos] = word_frequency.get(word_pos, 0) + 1
        pos_count[pos] = pos_count.get(pos, 0) + 1

    most_common_word = max(word_frequency, key=word_frequency.get).split('_')[0]
    least_common_word = min(word_frequency, key=word_frequency.get).split('_')[0]
    most_common_word_pos = max(word_frequency, key=word_frequency.get).split('_')[1]
    least_common_word_pos = min(word_frequency, key=word_frequency.get).split('_')[1]
    word_count = sum(word_frequency.values())

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
                text=f"Cantidad total de palabras: {word_count}    Palabra más usada: {most_common_word} [{word_frequency.get(most_common_word, 0)}] ({POS_LABELS.get(most_common_word_pos, most_common_word_pos)})    Palabra menos usada: {least_common_word} [{word_frequency.get(least_common_word, 0)}] ({POS_LABELS.get(least_common_word_pos, least_common_word_pos)})",
                showarrow=False,
                font=dict(size=12)
            )
        ],
        legend_title_text='Categorías Gramaticales'
    )

    return fig
# Path: modules/syntax_analysis.py