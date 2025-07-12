import sys
import os
from downloader import download_audio_from_youtube
from transcriber import transcribe_audio
from summarizer import get_summary, get_topics
from speaker_identifier import detectar_hablantes_con_llama


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <URL de YouTube>")
        sys.exit(1)

    url = sys.argv[1]

    print("[1] Descargando audio de YouTube...")
    audio_path = download_audio_from_youtube(url)

    print("\n[2] Transcribiendo audio...")
    result = transcribe_audio(audio_path)
    segments = result["segments"]
    transcript = " ".join(seg["text"] for seg in segments)



    print("\n[3] Generando resumen...")
    summary = get_summary(transcript)

    print("\n[4] Extrayendo temas clave...")
    topics = get_topics(transcript)


    print("\n[5] Identificando hablantes...")
    transcripcion_con_hablantes = detectar_hablantes_con_llama(segments)

    print("\n===== TRANSCRIPCIÓN CON HABLANTES =====")
    print(transcripcion_con_hablantes)


    print("\n===== RESUMEN =====")
    print(summary)


    guardar_resultados(audio_path, transcript, summary, topics, transcripcion_con_hablantes)


def guardar_resultados(audio_path, transcripcion, resumen, temas, con_hablantes):
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    output_path = os.path.join("resultados", f"{base_name}.txt")
    os.makedirs("resultados", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("===== TRANSCRIPCIÓN =====\n")
        f.write(transcripcion + "\n\n")
        f.write("===== RESUMEN =====\n")
        f.write(resumen + "\n\n")
        f.write("===== TEMAS CLAVE =====\n")
        f.write(temas + "\n\n")
        f.write("===== TRANSCRIPCIÓN CON HABLANTES =====\n")
        f.write(con_hablantes + "\n")

    print(f"\n[✓] Resultados guardados en: {output_path}")

if __name__ == "__main__":
    main()
