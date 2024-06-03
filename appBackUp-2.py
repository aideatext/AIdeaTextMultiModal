import gradio as gr
import requests

# URL de tu función Lambda
LAMBDA_URL = "https://5f6b6akff7.execute-api.us-east-2.amazonaws.com/DEV/morphAnalyzer"

# Función para hacer la solicitud a la función Lambda del análisis morfológico
def analisis_morfologico(text):
    response = requests.post(LAMBDA_URL, json={"text": text})
    if response.status_code == 200:
        result = response.json()
        return result['morph']  # Aquí asumes que 'morph' es el gráfico devuelto por la función Lambda
    else:
        return f"Error: {response.json().get('error', 'No se pudo realizar el análisis')}"

# Configurar la interfaz de usuario
with gr.Blocks(title="AIdeaText - Análisis de Texto") as demo:
    # Personalizar favicon y título
    gr.HTML("""
    <link rel="icon" type="image/x-icon" href="assets/icoV1.ico">
    <style>
        body { font-family: Arial, sans-serif; }
        #logo { width: 32px; height: 32px; }
    </style>
    """)

    # Encabezado con logo, título y subtítulo
    with gr.Row():
        gr.Image("assets/img/logoV3.png", elem_id="logo", width=32, height=32)
        with gr.Column():
            gr.Markdown("<h1>AIdeaText</h1>")
            gr.Markdown("<h3 style='margin-top: 0;'>Una herramienta de análisis de texto avanzada</h3>")
            gr.HTML("<hr>")

    # Configurar las pestañas de análisis
    with gr.Tabs():
        with gr.TabItem("Procesamiento de Texto"):
            with gr.Tabs():
                with gr.TabItem("Análisis Morfológico"):
                    text_input = gr.Textbox(lines=5, placeholder="Ingrese el texto aquí...", elem_id="text-morph")
                    output = gr.HTML(elem_id="network-morph")  # Aquí se mostrará el gráfico
                    button = gr.Button("Obtener análisis morfolófico", elem_id="ButtonMorph")
                    button.click(analisis_morfologico, inputs=text_input, outputs=output)

    gr.Markdown("### Pie de página - AIdeaText")
    gr.HTML("""
    <script src="assets/js/visualizeMorph.js"></script>
    """)

# Ejecutar la aplicación
demo.launch(server_name="127.0.0.1", server_port=7860)
