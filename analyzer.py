from llama_cpp import Llama

# Cargar el mismo modelo que en summarizer.py
llm = Llama(
    model_path="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_ctx=32768,
    n_threads=6,
    n_gpu_layers=30
)

def extract_keywords(text, max_tokens=256):
    prompt = f"""
[INST] Lee el siguiente texto en español y responde con una lista de 5 temas clave o palabras clave que resumen el contenido. Usa frases o etiquetas cortas. No expliques ni formules preguntas.

Texto:
{text.strip()}

Palabras clave: [/INST]
"""
    response = llm(prompt, max_tokens=max_tokens, temperature=0.7, stop=["</s>"])
    return response["choices"][0]["text"].strip()
