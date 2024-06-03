import spacy

def download_models():
    spacy.cli.download("es_core_news_lg")
    spacy.cli.download("en_core_web_trf")

if __name__ == "__main__":
    download_models()
