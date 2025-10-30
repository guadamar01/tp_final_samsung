import os
import tempfile
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def speech_to_text(audio_bytes: bytes) -> str:
    """
    Convierte bytes de audio de Telegram a texto usando Groq Whisper sin FFmpeg.
    """
    # Guardar el audio temporalmente
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name

    # Llamar a la API Groq (usa Whisper detrás)
    with open(temp_audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file,
            language="es"
        )

    return transcription.text

