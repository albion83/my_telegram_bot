from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from dotenv import load_dotenv
import os

# Carga las variables del archivo .env
load_dotenv()

TOKEN = os.getenv("TOKEN")  # Saca el token desde la variable de entorno

bot = Bot(token=TOKEN)
app = Flask(__name__)

dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

def start(update, context):
    nombre = update.effective_user.first_name
    mensaje = (
        f"Hola {nombre}, ¡bienvenido a Pablo Analytics Bot! 👋\n\n"
        "📊 Soy tu asistente personal para conocer más sobre mí, mis servicios en análisis de datos y cómo puedo ayudarte.\n\n"
        "Usá los comandos disponibles para navegar:\n"
        "/info - Sobre mí\n"
        "/cv - Ver mi CV\n"
        "/servicios - Qué ofrezco\n"
        "/contacto - Cómo contactarme\n"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje)

dispatcher.add_handler(CommandHandler("start", start))

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "Bot de Pablo está funcionando."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Usar puerto de Render o 5000 localmente
    app.run(host="0.0.0.0", port=port, debug=True)
