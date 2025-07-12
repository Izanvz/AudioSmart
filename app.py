import streamlit as st
import os
from downloader import download_audio_from_youtube
from transcriber import transcribe_audio
from summarizer import get_summary, get_topics
from speaker_identifier import detectar_hablantes_con_llama
import json

# Idiomas compatibles (para Whisper y Mistral)
IDIOMAS_SOPORTADOS = {
    "Español": "es",
    "Inglés": "en",
    "Francés": "fr",
    "Italiano": "it",
    "Portugués": "pt",
    "Alemán": "de",
    "Catalán": "ca",
}


st.set_page_config(page_title="AudioSmart", layout="wide")
st.title("🎧 AudioSmart - Análisis Inteligente de Audio")

# Selector de idioma
idioma = st.selectbox("Selecciona el idioma del audio", list(IDIOMAS_SOPORTADOS.keys()))
idioma_codigo = IDIOMAS_SOPORTADOS[idioma]


# --- Estado de sesión para almacenar la ruta del audio ---
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

# --- Entrada: YouTube o archivo ---
modo = st.radio("¿Cómo quieres cargar el audio?", ["Desde YouTube", "Desde archivo"])

if modo == "Desde YouTube":
    url = st.text_input("Pega aquí el enlace del video")
    if st.button("Descargar audio de YouTube"):
        if url:
            st.session_state.audio_path = download_audio_from_youtube(url)
            st.success("Audio descargado correctamente.")
        else:
            st.warning("Debes ingresar una URL de YouTube.")

elif modo == "Desde archivo":
    uploaded_file = st.file_uploader("Sube un archivo de audio", type=["mp3", "wav"])
    if uploaded_file:
        os.makedirs("temp_audio", exist_ok=True)
        temp_path = f"temp_audio/{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
        st.session_state.audio_path = temp_path
        st.success("Archivo cargado correctamente.")

# --- Procesamiento (solo si ya hay un audio cargado) ---
if st.session_state.audio_path:
    if st.button("Procesar audio"):
        with st.spinner("Transcribiendo..."):
            result = transcribe_audio(st.session_state.audio_path, idioma_codigo)
            segments = result["segments"]
            transcript = " ".join(seg["text"] for seg in segments)

        with st.spinner("Generando resumen..."):
            summary = get_summary(transcript)

        with st.spinner("Extrayendo temas clave..."):
            topics = get_topics(transcript)

        with st.spinner("Identificando hablantes..."):
            hablantes = detectar_hablantes_con_llama(segments)

        # Resultados
        st.subheader("📝 Transcripción")
        st.text_area("Texto completo", transcript, height=300)

        st.subheader("📌 Resumen")
        st.markdown(summary)

        st.subheader("🔑 Temas clave")
        st.markdown(topics)

        st.subheader("🗣️ Diálogo con hablantes identificados")
        st.text_area("Hablantes", hablantes, height=300)

        st.success("¡Análisis completo!")

        # --- Descarga de resultados ---
        st.subheader("💾 Descargar resultados")

        resultado_txt = f"""===== TRANSCRIPCIÓN =====\n{transcript}\n\n===== RESUMEN =====\n{summary}\n\n===== TEMAS CLAVE =====\n{topics}\n\n===== TRANSCRIPCIÓN CON HABLANTES =====\n{hablantes}"""

        resultado_json = {
            "idioma": idioma,
            "transcripcion": transcript,
            "resumen": summary,
            "temas_clave": topics,
            "hablantes": hablantes
        }

        st.download_button("📄 Descargar como .txt", resultado_txt, file_name="resultado.txt")
        st.download_button("🧾 Descargar como .json", json.dumps(resultado_json, indent=2, ensure_ascii=False), file_name="resultado.json")

        # --- Botón para reiniciar la app ---
        if st.button("🔄 Reiniciar aplicación"):
            st.session_state.clear()
            st.experimental_rerun()

