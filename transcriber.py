import whisperx
import torch

def transcribe_audio(audio_path, language=None):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float32"

    print(f"[INFO] Usando dispositivo: {device} | Precisión: {compute_type}")
    model = whisperx.load_model("medium", device=device, compute_type=compute_type, language=language)

    result = model.transcribe(audio_path)
    return result


