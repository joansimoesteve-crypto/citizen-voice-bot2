import streamlit as st
from datetime import datetime
import pandas as pd
import os

# CONFIGURACIÓN INICIAL
st.set_page_config(page_title="Urna Digital", page_icon="🗳️")

# ESTILO VISUAL
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f8;
    }
    h1 {
        text-align: center;
        color: #1f3c88;
    }
    .stButton>button {
        background-color: #1f3c88;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# TÍTULO
st.title("🗳️ URNA DIGITAL")
st.caption("Pon tu móvil y habla. Tu voz mejora esta ciudad.")

# INICIALIZAR ESTADO
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.area = ""
    st.session_state.tipo = ""
    st.session_state.descripcion = ""
    st.session_state.puntuacion = ""

# PASO 1 — ÁREA
if st.session_state.step == 1:
    st.markdown("💬 **Hola. Soy la Urna Digital.**")
    st.markdown("¿Sobre qué área quieres opinar?")

    area = st.selectbox(
        "",
        ["Urbanismo", "Limpieza", "Movilidad", "Seguridad", "Parques", "Otra"]
    )

    if st.button("Continuar"):
        st.session_state.area = area
        st.session_state.step = 2

# PASO 2 — TIPO
elif st.session_state.step == 2:
    st.markdown("💬 ¿Quieres informar de una incidencia o hacer una propuesta?")

    tipo = st.radio(
        "",
        ["Informar de una incidencia", "Hacer una propuesta"]
    )

    if st.button("Continuar"):
        st.session_state.tipo = tipo
        st.session_state.step = 3

# PASO 3 — DESCRIPCIÓN
elif st.session_state.step == 3:
    st.markdown("💬 Describe la incidencia o propuesta con el mayor detalle posible.")

    descripcion = st.text_area("")

    if st.button("Continuar"):
        st.session_state.descripcion = descripcion
        st.session_state.step = 4

# PASO 4 — PUNTUACIÓN
elif st.session_state.step == 4:
    st.markdown("💬 ¿Cómo valoras el servicio global? (1 = Muy malo, 5 = Excelente)")

    puntuacion = st.slider("", 1, 5)

    if st.button("Enviar"):
        st.session_state.puntuacion = puntuacion
        st.session_state.step = 5

# PASO FINAL — GUARDAR DATOS
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

    st.success("✅ Gracias por participar.")
    st.write("Tu voz mejora esta ciudad.")

    if st.button("Nueva respuesta"):
        st.session_state.step = 1
