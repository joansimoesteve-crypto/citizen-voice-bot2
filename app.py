import streamlit as st
from datetime import datetime
import pandas as pd
import os

st.set_page_config(page_title="Urna Digital", page_icon="🗳️")

# 🎨 ESTILO VERDE + BURBUJAS
st.markdown("""
<style>
body {
    background-color: #eef2f3;
}

.chatbot {
    max-width: 600px;
    margin: auto;
}

.bot-bubble {
    background-color: #e6f4ea;
    padding: 12px 16px;
    border-radius: 15px 15px 15px 5px;
    margin-bottom: 10px;
    width: fit-content;
}

.user-bubble {
    background-color: #1faa59;
    color: white;
    padding: 12px 16px;
    border-radius: 15px 15px 5px 15px;
    margin-left: auto;
    margin-bottom: 10px;
    width: fit-content;
}

.stButton>button {
    background-color: #1faa59;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

st.title("🗳️ URNA DIGITAL")
st.caption("Pon tu móvil y habla. Tu voz mejora esta ciudad.")

if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.area = ""
    st.session_state.tipo = ""
    st.session_state.descripcion = ""
    st.session_state.puntuacion = ""

st.markdown('<div class="chatbot">', unsafe_allow_html=True)

# PASO 1
if st.session_state.step == 1:
    st.markdown('<div class="bot-bubble">Hola 👋 Soy la Urna Digital.<br>¿Sobre qué área quieres opinar?</div>', unsafe_allow_html=True)

    area = st.selectbox("", ["Urbanismo", "Limpieza", "Movilidad", "Seguridad", "Parques", "Otra"])

    if st.button("Enviar"):
        st.session_state.area = area
        st.session_state.step = 2

# PASO 2
elif st.session_state.step == 2:
    st.markdown(f'<div class="user-bubble">{st.session_state.area}</div>', unsafe_allow_html=True)
    st.markdown('<div class="bot-bubble">¿Quieres informar de una incidencia o hacer una propuesta?</div>', unsafe_allow_html=True)

    tipo = st.radio("", ["Incidencia", "Propuesta"])

    if st.button("Enviar"):
        st.session_state.tipo = tipo
        st.session_state.step = 3

# PASO 3
elif st.session_state.step == 3:

    st.markdown(f'<div class="user-bubble">{st.session_state.area}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="user-bubble">{st.session_state.tipo}</div>', unsafe_allow_html=True)

    st.markdown('<div class="bot-bubble">Describe tu mensaje usando voz o texto.</div>', unsafe_allow_html=True)

    # Campo donde se mostrará la transcripción
    descripcion = st.text_area("Tu mensaje aparecerá aquí:", key="descripcion_texto")

    # BOTÓN DE VOZ (Web Speech API)
    st.components.v1.html("""
        <script>
        var recognition;
        function startRecognition() {
            recognition = new webkitSpeechRecognition();
            recognition.lang = "es-ES";
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            recognition.onresult = function(event) {
                var transcript = event.results[0][0].transcript;
                const textarea = window.parent.document.querySelector('textarea');
                textarea.value = transcript;
                textarea.dispatchEvent(new Event('input', { bubbles: true }));
            };

            recognition.start();
        }
        </script>

        <button onclick="startRecognition()" 
        style="background-color:#1faa59;color:white;
        border:none;padding:12px 20px;
        border-radius:30px;font-size:16px;">
        🎤 Hablar
        </button>
    """, height=80)

    if st.button("Continuar"):
        st.session_state.descripcion = descripcion
        st.session_state.step = 4

# PASO 4
elif st.session_state.step == 4:
    st.markdown(f'<div class="user-bubble">{st.session_state.area}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="user-bubble">{st.session_state.tipo}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="user-bubble">{st.session_state.descripcion}</div>', unsafe_allow_html=True)
    st.markdown('<div class="bot-bubble">¿Cómo valoras el servicio global? (1-5)</div>', unsafe_allow_html=True)

    puntuacion = st.slider("", 1, 5)

    if st.button("Enviar y finalizar"):
        st.session_state.puntuacion = puntuacion
        st.session_state.step = 5

# FINAL
elif st.session_state.step == 5:

    data = {
        "fecha": datetime.now(),
        "area": st.session_state.area,
        "tipo": st.session_state.tipo,
        "descripcion": st.session_state.descripcion,
        "puntuacion": st.session_state.puntuacion
    }

    df = pd.DataFrame([data])
    file = "respuestas.csv"

    if os.path.exists(file):
        df.to_csv(file, mode="a", header=False, index=False)
    else:
        df.to_csv(file, index=False)

    st.markdown('<div class="bot-bubble">✅ Gracias por participar. Tu voz mejora esta ciudad.</div>', unsafe_allow_html=True)

    if st.button("Nueva conversación"):
        st.session_state.step = 1

st.markdown('</div>', unsafe_allow_html=True)
