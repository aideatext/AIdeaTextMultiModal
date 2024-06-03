import requests

LAMBDA_URL = "https://5f6b6akff7.execute-api.us-east-2.amazonaws.com/DEV/syntaxAnalyzer"

def analisis_sintactico(text):
    response = requests.post(LAMBDA_URL, json={"text": text})
    if response.status_code == 200:
        svg = response.content.decode('utf-8')
        return f'<div style="width: 100%; height: 100%; overflow: auto;">{svg}</div>'
    else:
        return f"Error: {response.json().get('error', 'No se pudo realizar el análisis')}"

# Configuración de la interfaz de Gradio
#iface = gr.Interface(
#    fn=analisis_sintactico,
#    inputs="textbox",
#    outputs="html",
#    title="Análisis Sintáctico con Displacy"
#)

#iface.launch()
