from llama_cpp import Llama

# Ruta al modelo GGUF
llm = Llama(
    model_path="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_ctx=32768,
    n_threads=6,
    n_gpu_layers=30
)

def construir_transcripcion_segmentada(segments):
    texto = ""
    for seg in segments:
        start = f"{seg['start']:.2f}s"
        end = f"{seg['end']:.2f}s"
        texto += f"[{start}–{end}] {seg['text'].strip()}\n"
    return texto.strip()

def detectar_hablantes_con_llama(segments, max_tokens=2048):
    texto_segmentado = construir_transcripcion_segmentada(segments)

    prompt = f"""
A continuación tienes una transcripción con marcas de tiempo. Tu tarea es identificar a los diferentes hablantes.Pueden ser uno o varios, si alguno se presenta por su nombre (por ejemplo: "Soy Pedro"), usa ese nombre. Si no hay nombre, asígnales etiquetas como "Hablante 1", "Hablante 2", etc. Reescribe la transcripción asignando claramente cada intervención al hablante correspondiente.

Texto:
{texto_segmentado}

Transcripción con hablantes identificados:
"""
    respuesta = llm(prompt, max_tokens=max_tokens, temperature=0.7, stop=["</s>"])
    return respuesta["choices"][0]["text"].strip()
