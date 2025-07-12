import os
import yt_dlp
from pydub import AudioSegment

def sanitize_filename(title):
    return "".join(c for c in title if c.isalnum() or c in " -_").rstrip()

def download_audio_from_youtube(url, output_dir="audios", convert_to="wav"):
    os.makedirs(output_dir, exist_ok=True)

    # Obtener info sin descargar
    ydl_opts_info = {'quiet': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(url, download=False)
        title = sanitize_filename(info["title"])
        mp3_path = os.path.join(output_dir, f"{title}.mp3")
        wav_path = os.path.join(output_dir, f"{title}.wav")

    # Caso 1: ya existe .wav
    if os.path.exists(wav_path):
        print(f"[✓] Audio .wav ya existe: {wav_path}")
        return wav_path

    # Caso 2: existe .mp3 → convertir a .wav
    if os.path.exists(mp3_path):
        print(f"[→] Encontrado .mp3, convirtiendo a .wav...")
        sound = AudioSegment.from_mp3(mp3_path)
        sound.export(wav_path, format="wav")
        return wav_path

    # Caso 3: no existe nada → descargar y convertir
    print("[↓] Descargando audio desde YouTube...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, f'{title}.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")
    return wav_path
