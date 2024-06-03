import streamlit as st
from PIL import Image
import traceback
import re
import torch
from transformers import AutoModel, AutoTokenizer, pipeline

def initialize_model(device='cpu', dtype='float32'):
    if device != 'cpu':
        raise ValueError("Invalid device. Use 'cpu'.")

    dtype = torch.float32

    # Load model
    # model_path = 'openbmb/MiniCPM-V-2'
    # model = AutoModel.from_pretrained(model_path, trust_remote_code=True).to(dtype=dtype)
    # tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

    # Load model
    model = AutoModel.from_pretrained("openbmb/MiniCPM-V-2", trust_remote_code=True).to(dtype=dtype)
    tokenizer = AutoTokenizer.from_pretrained("openbmb/MiniCPM-V-2", trust_remote_code=True)
    pipe = pipeline("visual-question-answering", model=model, tokenizer=tokenizer, device=-1 if device == 'cpu' else 0)

    model = model.to(device=device, dtype=dtype)
    model.eval()

    return model, tokenizer, device, dtype

# Initialize model with default values
model, tokenizer, device, dtype = initialize_model()

ERROR_MSG = "Error, please retry"
model_name = 'MiniCPM-V 2.0'

def chat(img, msgs, params=None):
    default_params = {"num_beams": 3, "repetition_penalty": 1.2, "max_new_tokens": 1024}
    if params is None:
        params = default_params
    if img is None:
        return -1, "Error, invalid image, please upload a new image"
    try:
        image = img.convert('RGB')
        with torch.no_grad():
            answer, _, _ = model.chat(
                image=image,
                msgs=msgs,
                context=None,
                tokenizer=tokenizer,
                **params
            )
        answer = re.sub(r'(<.*?>)', '', answer)  # Remove any HTML tags
        return 0, answer
    except Exception as err:
        print(err)
        traceback.print_exc()
        return -1, ERROR_MSG

def upload_img(image, chat_history, session_state):
    image = Image.open(image)
    session_state['image'] = image
    chat_history.append(('', 'Image uploaded successfully, you can talk to me now'))
    return chat_history, session_state

def respond(question, chat_history, session_state, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature):
    if 'image' not in session_state:
        chat_history.append((question, 'Please upload an image to start'))
        return '', chat_history, session_state

    context = [{"role": "user", "content": question}]
    print('<User>:', question)

    params = {
        'sampling': params_form == 'Sampling',
        'num_beams': num_beams,
        'repetition_penalty': repetition_penalty if params_form == 'Beam Search' else repetition_penalty_2,
        'top_p': top_p,
        'top_k': top_k,
        'temperature': temperature,
        "max_new_tokens": 896
    }
    code, answer = chat(session_state['image'], context, params)
    print('<Assistant>:', answer)

    context.append({"role": "assistant", "content": answer})
    chat_history.append((question, answer))
    return '', chat_history, session_state

def regenerate_button_clicked(question, chat_history, session_state, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature):
    if len(chat_history) <= 1:
        chat_history.append(('Regenerate', 'No question for regeneration.'))
        return '', chat_history, session_state
    elif chat_history[-1][0] == 'Regenerate':
        return '', chat_history, session_state
    else:
        question = chat_history[-1][0]
        chat_history = chat_history[:-1]
    return respond(question, chat_history, session_state, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature)

def create_image_analysis_interface(uploaded_image):
    st.sidebar.header("Configuración del Análisis de Imágenes")

    with st.sidebar:
        params_form = st.radio("Decode Type", ('Beam Search', 'Sampling'))
        num_beams = st.slider('Num Beams', 0, 5, 3)
        repetition_penalty = st.slider('Repetition Penalty', 0.0, 3.0, 1.2)
        repetition_penalty_2 = st.slider('Repetition Penalty 2', 0.0, 3.0, 1.05)
        max_new_tokens = st.slider('Max New Tokens', 1, 4096, 1024)
        top_p = st.slider('Top P', 0.0, 1.0, 0.8)
        top_k = st.slider('Top K', 0, 200, 100)
        temperature = st.slider('Temperature', 0.0, 2.0, 0.7)

    # Initialize chat history if not present
    if 'chat' not in st.session_state:
        st.session_state['chat'] = []

    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.session_state['image'] = image

    input_text = st.text_input("Input text", key="input_text")

    if st.button("Enviar"):
        input_text, st.session_state['chat'], st.session_state = respond(input_text, st.session_state['chat'], st.session_state, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature)

    for question, answer in st.session_state['chat']:
        st.write(f"**You:** {question}")
        st.write(f"**Assistant:** {answer}")
        st.write("----")

    if st.button("Regenerate"):
        _, st.session_state['chat'], st.session_state = regenerate_button_clicked(input_text, st.session_state['chat'], st.session_state, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature)

    if st.button("Clear Chat"):
        st.session_state['chat'] = []

    st.write("----")
