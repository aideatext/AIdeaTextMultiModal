import spacy
import spacy_streamlit

# Cargar el modelo spaCy localmente
nlp = spacy.load("es_core_news_lg")

def analisis_sintactico(text):
    doc = nlp(text)
    return doc
