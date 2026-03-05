import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Urna Digital", page_icon="🗳️")

# ===== ESTILO CHAT =====

st.markdown("""
<style>

.bot{
background:#f1f1f1;
padding:12px;
border-radius:15px;
margin-bottom:10px;
width:fit-content;
}

.user{
background:#1faa59;
color:white;
padding:12px;
border-radius:15px;
margin-bottom:10px;
margin-left:auto;
width:fit-content;
}

</style>
""", unsafe_allow_html=True)

st.title("🗳️ Urna Digital")
st.caption("Pon tu móvil y habla. Tu voz mejora la ciudad.")

# ===== ESTADO =====

if "area" not in st.session_state:
    st.session_state.area=None

if "tipo" not in st.session_state:
    st.session_state.tipo=None

if "descripcion" not in st.session_state:
    st.session_state.descripcion=""

if "puntuacion" not in st.session_state:
    st.session_state.puntuacion=3

# ===== PASO 1 =====

st.markdown('<div class="bot">¿Sobre qué área quieres opinar?</div>', unsafe_allow_html=True)

area = st.selectbox(
"",
["Selecciona","Urbanismo","Limpieza","Movilidad","Seguridad","Parques","Otra"]
)

if area!="Selecciona":

    st.session_state.area=area
    st.markdown(f'<div class="user">{area}</div>', unsafe_allow_html=True)

# ===== PASO 2 =====

if st.session_state.area:

    st.markdown('<div class="bot">¿Es una incidencia o una propuesta?</div>', unsafe_allow_html=True)

    tipo = st.selectbox(
    "",
    ["Selecciona","Incidencia","Propuesta"]
    )

    if tipo!="Selecciona":

        st.session_state.tipo=tipo
        st.markdown(f'<div class="user">{tipo}</div>', unsafe_allow_html=True)

# ===== PASO 3 =====

if st.session_state.tipo:

    st.markdown('<div class="bot">Describe el problema o propuesta. Puedes hablar.</div>', unsafe_allow_html=True)

    descripcion = st.text_area("")

    st.components.v1.html("""

<script>

function startDictation() {

if (window.hasOwnProperty('webkitSpeechRecognition')) {

var recognition = new webkitSpeechRecognition();

recognition.lang = "es-ES";

recognition.onresult = function(e) {

var text = e.results[0][0].transcript;

const textarea = window.parent.document.querySelector('textarea');

textarea.value = text;

textarea.dispatchEvent(new Event('input', { bubbles: true }));

};

recognition.start();

}

}

</script>

<button onclick="startDictation()" style="background:#1faa59;color:white;padding:10px;border-radius:20px;border:none;">
🎤 Hablar
</button>

""", height=80)

    st.session_state.descripcion=descripcion

# ===== PASO 4 =====

if st.session_state.descripcion:

    st.markdown('<div class="bot">¿Cómo valoras el servicio?</div>', unsafe_allow_html=True)

    puntuacion = st.slider("",1,5,3)

    st.session_state.puntuacion=puntuacion

# ===== LOCALIZACION =====

st.markdown('<div class="bot">Detectar ubicación 📍</div>', unsafe_allow_html=True)

loc = st.components.v1.html("""

<script>

navigator.geolocation.getCurrentPosition(function(position) {

const coords = position.coords.latitude + "," + position.coords.longitude;

window.parent.postMessage(coords, "*");

});

</script>

""", height=0)

# ===== GUARDAR =====

if st.button("Enviar opinión"):

    data = {
        "fecha":datetime.now(),
        "area":st.session_state.area,
        "tipo":st.session_state.tipo,
        "descripcion":st.session_state.descripcion,
        "puntuacion":st.session_state.puntuacion
    }

    df=pd.DataFrame([data])

    archivo="respuestas.csv"

    if os.path.exists(archivo):

        df.to_csv(archivo,mode="a",header=False,index=False)

    else:

        df.to_csv(archivo,index=False)

    st.success("Gracias. Tu voz mejora la ciudad.")
