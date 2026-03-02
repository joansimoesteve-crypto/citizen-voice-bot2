import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.title("🎤 CitizenVoice")

st.write("Pulsa para grabar tu opinión sobre tu municipio.")

audio = st.file_uploader("Sube tu audio", type=["wav","mp3","m4a"])

if audio is not None:
    st.success("Audio recibido.")

    # Guardar archivo
    file_name = f"audio_{datetime.now().strftime('%Y%m%d%H%M%S')}.wav"
    with open(file_name, "wb") as f:
        f.write(audio.read())

    # Guardar registro
    df = pd.DataFrame([[file_name, datetime.now()]], columns=["audio_file","timestamp"])
    df.to_csv("respuestas.csv", mode="a", header=not os.path.exists("respuestas.csv"), index=False)

    st.write("Gracias por participar 🙌")
