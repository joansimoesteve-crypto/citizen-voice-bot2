import streamlit as st
from datetime import datetime
import pandas as pd
import os

st.set_page_config(page_title="Urna Digital", page_icon="🗳️")

# ESTILO VERDE + BURBUJAS + BOTONES CIRCULARES
st.markdown("""
<style>
body { background-color: #eef2f3; }
.chatbot { max-width: 600px; margin: auto; }
.bot-bubble { background-color: #e6f4ea; padding: 12px 16px; border-radius: 15px 15px 15px 5px; margin-bottom: 10px; width: fit-content; }
.user-bubble { background-color: #1faa59; color: white; padding: 12px 16px; border-radius: 15px 15px 5px 15px; margin-left: auto; margin-bottom: 10px; width: fit-content; }
.stButton>button { background-color: #1faa59; color: white; border-radius: 10px; height: 3em; width: 100%; font-size: 16px; }
button.option { background-color: #1faa59; color: white; border:none; border-radius:30px; padding:12px 20px; margin:5px; font-size:16px; cursor:pointer; }
button.option:hover { background-color:#138844; }
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

# --- PASO 1: ÁREA ---
if st.session_state.step == 1:
    st.markdown('<div class="bot-bubble">Hola 👋 Soy la Urna Digital.<br>¿Sobre qué área quieres opinar?</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    areas = ["Urbanismo","Limpieza","Movilidad","Seguridad","Parques","Otra"]
    for i, area in enumerate(areas):
        if cols[i%3].button(area, key=f"area_{area}", help="Selecciona esta área"):
            st.session_state.area = area
            st.session_state.step = 2
            st.experimental_rerun()

# --- PASO 2: TIPO ---
elif st.session_state.step == 2:
    st.markdown(f'<div class="user-bubble">{st.session_state.area}</div>', unsafe_allow_html=True)
    st.markdown('<div class="bot-bubble">¿Quieres informar de una incidencia o hacer una propuesta?</div>', unsafe_allow_html=True)

    cols = st.columns(2)
    tipos = ["Incidencia","Propuesta"]
    for i, tipo in enumerate(tipos):
        if cols[i].button(tipo, key=f"tipo_{tipo}"):
            st.session_state.tipo = tipo
            st.session_state.step = 3
            st.experimental_rerun()

# --- PASO 3: DESCRIPCIÓN (voz + texto) ---
elif st.session_state.step == 3:
    st.markdown(f'<div class="user-bubble">{st.session_state.area}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="user-bubble">{st.session_state.tipo}</div>', unsafe_allow_html=True)
    st.markdown('<div class="bot-bubble">Describe tu mensaje usando voz o texto.</div>', unsafe_allow_html=True)

    descripcion = st.text_area("Tu mensaje aparecerá aquí:", key="descripcion_texto")

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
        border-radius:30px;font-size:16px;margin-top:10px;">
        🎤 Hablar
        </button>
    """, height=80)

    if st.button("Continuar"):
        st.session_state.descripcion = descripcion
        st.session_state.step = 4

# --- PASO 4: PUNTUACIÓN ---
elif st.session_state.step == 4:
    st.markdown(f'<div class="user-bubble">{st.session_state.area}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="user-bubble">{st.session_state.tipo}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="user-bubble">{st.session_state.descripcion}</div>', unsafe_allow_html=True)
    st.markdown('<div class="bot-bubble">¿Cómo valoras el servicio global? (1 = Muy malo, 5 = Excelente)</div>', unsafe_allow_html=True)

    cols = st.columns(5)
    for i in range(1,6):
        if cols[i-1].button(str(i), key=f"punt_{i}"):
            st.session_state.puntuacion = i
            st.session_state.step = 5
            st.experimental_rerun()

# --- PASO 5: FINAL ---
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

    mensaje_final = "Gracias por participar. Tu voz mejora esta ciudad."

    st.markdown(f'<div class="bot-bubble">✅ {mensaje_final}</div>', unsafe_allow_html=True)

    # VOZ DEL BOT AL FINAL
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{mensaje_final}");
        msg.lang = "es-ES";
        msg.rate = 1;
        msg.pitch = 1;
        speechSynthesis.speak(msg);
        </script>
    """, height=0)

    if st.button("Nueva conversación"):
        st.session_state.step = 1

st.markdown('</div>', unsafe_allow_html=True)
