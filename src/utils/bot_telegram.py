import os
import telebot
from dotenv import load_dotenv
from services.speech2text import speech_to_text

# Cargar variables de entorno (.env)
load_dotenv()

# Crear el bot con el token de Telegram
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Mensaje de bienvenida
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "🎙️ ¡Hola! Enviame un audio y te diré lo que dijiste 😄")

# Handler para audios (notas de voz)
@bot.message_handler(content_types=['voice', 'audio'])
def handle_voice(message):
    try:
        print("📥 Recibido audio de:", message.from_user.username or message.from_user.first_name)
        print("Tipo:", message.content_type)

        # Obtener archivo del mensaje de voz
        file_info = bot.get_file(message.voice.file_id if message.content_type == 'voice' else message.audio.file_id)
        audio_bytes = bot.download_file(file_info.file_path)

        # Convertir audio a texto
        text = speech_to_text(audio_bytes)

        bot.reply_to(message, f"🗣️ Dijiste: {text}")

    except Exception as e:
        bot.reply_to(message, f"❌ Ocurrió un error: {e}")
        print("Error:", e)

# Iniciar el bot
if __name__ == "__main__":
    print("🤖 Bot con reconocimiento de voz activo...")
    bot.infinity_polling()
