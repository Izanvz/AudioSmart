from llama_cpp import Llama
import os

# Ruta al modelo .gguf descargado
MODEL_PATH = "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"

# Cargar el modelo con soporte extendido de contexto
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=32768,           # hasta 32k tokens
    n_threads=6,           # ajusta según tu CPU
    n_gpu_layers=30        # ajusta según tu GPU (usa VRAM)
)

def get_summary(text, max_tokens=1024):
    prompt = f"""
[INST] Resume el siguiente texto en español de forma clara, concisa y en tono profesional. No formules preguntas.

Texto:
{text.strip()}

Resumen: [/INST]
"""
    response = llm(prompt, max_tokens=max_tokens, temperature=0.7, stop=["</s>"])
    return response["choices"][0]["text"].strip()

def get_topics(text, max_tokens=256):
    prompt = f"""
[INST] Escribe una lista de 5 temas clave mencionados en el siguiente texto. Usa frases breves. No expliques ni formules preguntas.

Texto:
{text.strip()}

Temas clave: [/INST]
"""
    response = llm(prompt, max_tokens=max_tokens, temperature=0.7, stop=["</s>"])
    return response["choices"][0]["text"].strip()
