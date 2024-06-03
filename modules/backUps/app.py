import streamlit as st
import spacy
import spacy_streamlit
from spacy import displacy
#import streamlit.components.v1 as components

from modules.morph_analysis import analisis_morfologico
from modules.syntax_analysis import analisis_sintactico
from modules.semantic_analysis import analisis_semantico
from modules.discourse_analysis import procesar_discurso
from modules.image_analysis_CPU import create_image_analysis_interface

# Variables globales para el análisis de texto
nlp_es = spacy.load("es_core_news_lg")
nlp_en = spacy.load("en_core_web_trf")
nlp = nlp_es

setences_span = []
displacy.render(setences_span, style="dep", options={"compact": True, "color": "#000000", "bg": "#ffffff"})

# Función para cambiar el idioma del modelo spaCy
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
        col1, col2 = st.columns([2, 1])
        with col1:
            text_input = st.text_area("Ingrese el texto aquí...", key="text-morph")
        with col2:
            st.markdown("""
            ### Leyenda de Análisis Morfológico
            <div style='display: flex; flex-wrap: wrap;'>
                <div style='margin-right: 20px;'><strong>ADP:</strong> Preposición</div>
                <div style='margin-right: 20px;'><strong>DET:</strong> Determinante</div>
                <div style='margin-right: 20px;'><strong>CONJ:</strong> Conjunción</div>
                <div style='margin-right: 20px;'><strong>CCONJ:</strong> Conjunción Coordinante</div>
                <div style='margin-right: 20px;'><strong>SCONJ:</strong> Conjunción Subordinante</div>
                <div style='margin-right: 20px;'><strong>ADJ:</strong> Adjetivo</div>
                <div style='margin-right: 20px;'><strong>ADV:</strong> Adverbio</div>
                <div style='margin-right: 20px;'><strong>NOUN:</strong> Sustantivo</div>
                <div style='margin-right: 20px;'><strong>VERB:</strong> Verbo</div>
                <div style='margin-right: 20px;'><strong>PROPN:</strong> Nombre Propio</div>
                <div style='margin-right: 20px;'><strong>PRON:</strong> Pronombre</div>
                <div style='margin-right: 20px;'><strong>AUX:</strong> Auxiliar</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Procesar", key="ButtonMorph"):
            output = analisis_morfologico(text_input)
            st.plotly_chart(output, use_container_width=True)

    with subtab2:
        st.header("Análisis Sintáctico")
        col1, col2 = st.columns([2, 1])
        with col1:
            text_input = st.text_area("Ingrese el texto aquí...", key="text-syntax")
            if st.button("Procesar", key="ButtonSyntax"):
                doc = analisis_sintactico(text_input)
                spacy_streamlit.visualize_parser(doc, title="Visualización del análisis sintáctico", displacy_options={"compact": True, "color": "#000000", "bg": "#ffffff"})
        with col2:
            st.markdown("""
            ### Leyenda de Relaciones Sintácticas
            <div style='display: flex; flex-wrap: wrap;'>
                <div style='margin-right: 20px;'><strong>nmod:</strong> modificador nominal</div>
                <div style='margin-right: 20px;'><strong>case:</strong> caso</div>
                <div style='margin-right: 20px;'><strong>conj:</strong> conjunción</div>
                <div style='margin-right: 20px;'><strong>cc:</strong> coordinación</div>
                <div style='margin-right: 20px;'><strong>acl:</strong> cláusula adjetiva</div>
                <div style='margin-right: 20px;'><strong>det:</strong> determinante</div>
                <div style='margin-right: 20px;'><strong>punct:</strong> puntuación</div>
                <div style='margin-right: 20px;'><strong>nsubj:</strong> sujeto nominal</div>
                <div style='margin-right: 20px;'><strong>aux:</strong> auxiliar</div>
                <div style='margin-right: 20px;'><strong>iobj:</strong> objeto indirecto</div>
                <div style='margin-right: 20px;'><strong>xcomp:</strong> complemento abierto</div>
            </div>
            """, unsafe_allow_html=True)

    with subtab3:
        st.header("Análisis Semántico")
        col1, col2 = st.columns([2, 1])
        with col1:
            text_input = st.text_area("Ingrese el texto aquí...", key="text-semantic")
            if st.button("Procesar", key="ButtonSemantic"):
                output = analisis_semantico(text_input)
                st.markdown(output, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            ### Leyenda de Análisis Semántico
            <div style='display: flex; flex-wrap: wrap;'>
                <div style='margin-right: 20px;'><strong>Entidades:</strong> Identificación de nombres propios, lugares, organizaciones, etc.</div>
                <div style='margin-right: 20px;'><strong>Relaciones:</strong> Conexiones semánticas entre entidades identificadas</div>
                <div style='margin-right: 20px;'><strong>Sentimiento:</strong> Análisis de polaridad y emociones en el texto</div>
            </div>
            """, unsafe_allow_html=True)

    with subtab4:
        st.header("Análisis de Discurso")
        col1, col2 = st.columns([2, 1])
        with col1:
            text_input1 = st.text_area("Ingrese el texto patrón aquí...", key="text-discourse-1")
            text_input2 = st.text_area("Ingrese el texto a comparar aquí...", key="text-discourse-2")
            if st.button("Procesar Texto Patrón", key="ButtonDiscourse1"):
                output1 = procesar_discurso(text_input1)
                st.markdown(output1, unsafe_allow_html=True)
            if st.button("Procesar Texto a Comparar", key="ButtonDiscourse2"):
                output2 = procesar_discurso(text_input2)
                st.markdown(output2, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            ### Leyenda de Análisis de Discurso
            <div style='display: flex; flex-wrap: wrap;'>
                <div style='margin-right: 20px;'><strong>Cohesión:</strong> Cómo se conectan las partes del texto</div>
                <div style='margin-right: 20px;'><strong>Coherencia:</strong> Lógica y consistencia del texto</div>
                <div style='margin-right: 20px;'><strong>Intención del hablante:</strong> Propósito detrás del texto</div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.header("Análisis de Imágenes")
    create_image_analysis_interface()

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
