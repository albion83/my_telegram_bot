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

def info(update, context):
    mensaje = (
        "👨‍💻 *Sobre mí*\n"
        "Soy Pablo Norberto, especialista en análisis de datos con experiencia en proyectos de BI, dashboards y automatización.\n"
        "Me apasiona transformar datos en información clara y útil para la toma de decisiones."
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje, parse_mode='Markdown')

def cv(update, context):
    mensaje = (
        "📄 *Mi CV*\n"
        "Puedes ver mi CV completo en mi sitio web:\n"
        "https://curriculumvitae.pablopallitto.ar/\n\n"
        "También puedo enviarte un resumen por acá si lo deseas."
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje, parse_mode='Markdown')

def servicios(update, context):
    mensaje = (
        "💼 *Servicios*\n"
        "- Análisis de datos y visualización\n"
        "- Creación de dashboards interactivos\n"
        "- Automatización de procesos con Python y Power BI\n"
        "- Consultoría para toma de decisiones basada en datos"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje, parse_mode='Markdown')

def contacto(update, context):
    mensaje = (
        "📞 *Contacto*\n"
        "Email: pablo.n.pallitto@gmail.com\n"
        "LinkedIn: https://www.linkedin.com/in/pablo-pallitto/n"
        "Teléfono: +54 9 11 2251-2731\n\n"
        "Estoy disponible para proyectos, consultas y colaboraciones."
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje, parse_mode='Markdown')

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("info", info))
dispatcher.add_handler(CommandHandler("cv", cv))
dispatcher.add_handler(CommandHandler("servicios", servicios))
dispatcher.add_handler(CommandHandler("contacto", contacto))

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "Bot de Pablo está funcionando."

if __name__ == "__main__":
    app.run(debug=True)
