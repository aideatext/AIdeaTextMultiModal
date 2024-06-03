import streamlit as st
from PIL import Image
import traceback
import re
import torch
from transformers import AutoModel, AutoTokenizer

def initialize_model(device='cuda', dtype='bf16'):
    if device not in ['cuda', 'mps']:
        raise ValueError("Invalid device. Choose between 'cuda' or 'mps'.")

    if dtype == 'bf16':
        dtype = torch.bfloat16
    elif dtype == 'fp16':
        dtype = torch.float16
    else:
        raise ValueError("Invalid dtype. Choose between 'bf16' or 'fp16'.")

    # Load model
    model_path = 'openbmb/MiniCPM-V-2'
    model = AutoModel.from_pretrained(model_path, trust_remote_code=True).to(dtype=dtype)
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

    model = model.to(device=device, dtype=dtype)
    model.eval()

    return model, tokenizer, device, dtype

# Initialize model with default values
model, tokenizer, device, dtype = initialize_model()

ERROR_MSG = "Error, please retry"
model_name = 'MiniCPM-V 2.0'

def chat(img, msgs, ctx, params=None, vision_hidden_states=None):
    default_params = {"num_beams": 3, "repetition_penalty": 1.2, "max_new_tokens": 1024}
    if params is None:
        params = default_params
    if img is None:
        return -1, "Error, invalid image, please upload a new image", None, None
    try:
        image = img.convert('RGB')
        with torch.no_grad():
            answer, context, _ = model.chat(
                image=image,
                msgs=msgs,
                context=None,
                tokenizer=tokenizer,
                **params
            )
        res = re.sub(r'(<box>.*</box>)', '', answer)
        res = res.replace('<ref>', '')
        res = res.replace('</ref>', '')
        res = res.replace('<box>', '')
        answer = res.replace('</box>', '')
        return -1, answer, None, None
    except Exception as err:
        print(err)
        traceback.print_exc()
        return -1, ERROR_MSG, None, None
    finally:
        torch.cuda.empty_cache()

def upload_img(image, _chatbot, _app_session):
    image = Image.open(image)

    _app_session['sts'] = None
    _app_session['ctx'] = []
    _app_session['img'] = image
    _chatbot.append(('', 'Image uploaded successfully, you can talk to me now'))
    return _chatbot, _app_session

def respond(_question, _chat_bot, _app_cfg, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature):
    if _app_cfg.get('ctx', None) is None:
        _chat_bot.append((_question, 'Please upload an image to start'))
        return '', _chat_bot, _app_cfg

    _context = _app_cfg['ctx'].copy()
    if _context:
        _context.append({"role": "user", "content": _question})
    else:
        _context = [{"role": "user", "content": _question}]
    print('<User>:', _question)

    if params_form == 'Beam Search':
        params = {
            'sampling': False,
            'num_beams': num_beams,
            'repetition_penalty': repetition_penalty,
            "max_new_tokens": 896
        }
    else:
        params = {
            'sampling': True,
            'top_p': top_p,
            'top_k': top_k,
            'temperature': temperature,
            'repetition_penalty': repetition_penalty_2,
            "max_new_tokens": 896
        }
    code, _answer, _, sts = chat(_app_cfg['img'], _context, None, params)
    print('<Assistant>:', _answer)

    _context.append({"role": "assistant", "content": _answer})
    _chat_bot.append((_question, _answer))
    if code == 0:
        _app_cfg['ctx'] = _context
        _app_cfg['sts'] = sts
    return '', _chat_bot, _app_cfg

def regenerate_button_clicked(_question, _chat_bot, _app_cfg, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature):
    if len(_chat_bot) <= 1:
        _chat_bot.append(('Regenerate', 'No question for regeneration.'))
        return '', _chat_bot, _app_cfg
    elif _chat_bot[-1][0] == 'Regenerate':
        return '', _chat_bot, _app_cfg
    else:
        _question = _chat_bot[-1][0]
        _chat_bot = _chat_bot[:-1]
        _app_cfg['ctx'] = _app_cfg['ctx'][:-2]
    return respond(_question, _chat_bot, _app_cfg, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature)

def create_image_analysis_interface(uploaded_file):
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

    # Sección del chat
    upload_img(uploaded_file, st.session_state['chat'], st.session_state)

    input_text = st.text_input("Input text", key="input_text")

    if st.button("Enviar"):
        respond(input_text, st.session_state['chat'], st.session_state, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature)

    for i, (question, answer) in enumerate(st.session_state['chat']):
        st.write(f"**You:** {question}")
        st.write(f"**Assistant:** {answer}")
        st.write("----")
    return
