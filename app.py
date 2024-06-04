import streamlit as st
from streamlit.components.v1 import components
from spacy import load, displacy
from transformers import pipeline

from modules.morph_analysis import analisis_morfologico
from modules.syntax_analysis import analisis_sintactico
from modules.semantic_analysis import analisis_semantico
from modules.discourse_analysis import procesar_discurso
from modules.image_analysis_CPU import create_image_analysis_interface

# Variables globales para el análisis de texto
nlp_es = spacy.load("es_core_news_lg")
nlp_en = spacy.load("en_core_web_trf")
nlp = nlp_es

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

def set_language():
    global nlp
    lang = st.session_state["language"]
    if lang == "Español":
        nlp = nlp_es
    elif lang == "Inglés":
        nlp = nlp_en
    st.success(f"Idioma seleccionado: {lang}")

# Inicializar claves en session_state
if 'language' not in st.session_state:
    st.session_state['language'] = "Español"

if 'input_text' not in st.session_state:
    st.session_state['input_text'] = ""

if 'chat' not in st.session_state:
    st.session_state['chat'] = []

# Configurar la interfaz de usuario con Streamlit
st.set_page_config(page_title="AIdeaText - Análisis de Texto", layout="wide")
st.title("AIdeaText")
st.header("Una herramienta de análisis de texto avanzada")

# Selector de idioma
st.selectbox("Seleccionar Idioma", ["Español", "Inglés"], key="language", on_change=set_language)

# Pestañas principales
tab1, tab2 = st.tabs(["Análisis de Texto", "Análisis de Imágenes"])

with tab1:
    # Pestañas de análisis de texto
    subtab1, subtab2, subtab3, subtab4 = st.tabs(["Análisis Morfológico", "Análisis Sintáctico", "Análisis Semántico", "Análisis de Discurso"])

    with subtab1:
        st.header("Análisis Morfológico")
        text_input = st.text_area("Ingrese el texto aquí...", key="text-morph")
        if st.button("Procesar", key="ButtonMorph"):
            output = analisis_morfologico(text_input)
            st.plotly_chart(output, use_container_width=True)

    with subtab2:
        st.header("Análisis Sintáctico")
        text_input = st.text_area("Ingrese el texto aquí...", key="text-syntax")
        if st.button("Procesar", key="ButtonSyntax"):
            doc = analisis_sintactico(text_input)
            spacy_streamlit.visualize_parser(doc, title="Visualización del análisis sintáctico", displacy_options={"compact": True, "color": "#000000", "bg": "#ffffff", "collapse_punct": False, "collapse_phrases": False})

    with subtab3:
        st.header("Análisis Semántico")
        text_input = st.text_area("Ingrese el texto aquí...", key="text-semantic")
        if st.button("Procesar", key="ButtonSemantic"):
            output = analisis_semantico(text_input)
            st.markdown(output, unsafe_allow_html=True)

    with subtab4:
        st.header("Análisis de Discurso")
        col1, col2 = st.columns(2)
        with col1:
            text_input1 = st.text_area("Ingrese el texto patrón aquí...", key="text-discourse-1")
            if st.button("Procesar Texto Patrón", key="ButtonDiscourse1"):
                st.session_state['output1'] = procesar_discurso(text_input1)
            if 'output1' in st.session_state:
                st.markdown(st.session_state['output1'], unsafe_allow_html=True)

        with col2:
            text_input2 = st.text_area("Ingrese el texto a comparar aquí...", key="text-discourse-2")
            if st.button("Procesar Texto a Comparar", key="ButtonDiscourse2"):
                st.session_state['output2'] = procesar_discurso(text_input2)
            if 'output2' in st.session_state:
                st.markdown(st.session_state['output2'], unsafe_allow_html=True)

with tab2:
    st.header("Análisis de Imágenes")
    uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"], key="image_uploader_main")

    if uploaded_file is not None:
        st.session_state["uploaded_image"] = uploaded_file

    if "uploaded_image" in st.session_state:
        col1, col2 = st.columns([2, 3])
        with col1:
            # Sección del chat
            create_image_analysis_interface(st.session_state["uploaded_image"])
        with col2:
            # Visualización de la imagen
            st.image(st.session_state["uploaded_image"], use_column_width=True)

# CSS personalizado para ajustar el contenedor del SVG
st.markdown("""
<style>
    .displacy-container {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto !important;
    }
</style>
""", unsafe_allow_html=True)
