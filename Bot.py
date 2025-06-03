from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler
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
        "Selecciona una opción para conocer más:"
    )
    keyboard = [
        [InlineKeyboardButton("Sobre mí", callback_data='info')],
        [InlineKeyboardButton("CV", callback_data='cv')],
        [InlineKeyboardButton("Servicios", callback_data='servicios')],
        [InlineKeyboardButton("Contacto", callback_data='contacto')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje, reply_markup=reply_markup)

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
        "Email: pablo.pallitto@gmail.com\n"
        "LinkedIn: https://www.linkedin.com/in/pablo-pallitto\n\n"
        "Teléfono: +54 9 11 2251-2731\n\n"
        "Estoy disponible para proyectos, consultas y colaboraciones."
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje, parse_mode='Markdown')

# Maneja los callbacks cuando el usuario pulsa un botón
def button_handler(update, context):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == 'info':
        texto = (
            "👨‍💻 *Sobre mí*\n"
            "Soy Pablo Norberto, especialista en análisis de datos con experiencia en proyectos de BI, dashboards y automatización.\n"
            "Me apasiona transformar datos en información clara y útil para la toma de decisiones."
        )
    elif data == 'cv':
        texto = (
            "📄 *Mi CV*\n"
            "Puedes ver mi CV completo en mi sitio web:\n"
            "https://curriculumvitae.pablopallitto.ar/\n\n"
            "También puedo enviarte un resumen por acá si lo deseas."
        )
    elif data == 'servicios':
        texto = (
            "💼 *Servicios*\n"
            "- Análisis de datos y visualización\n"
            "- Creación de dashboards interactivos\n"
            "- Automatización de procesos con Python y Power BI\n"
            "- Consultoría para toma de decisiones basada en datos"
        )
    elif data == 'contacto':
        texto = (
            "📞 *Contacto*\n"
            "Email: pablo.pallitto@gmail.com\n"
            "LinkedIn: https://www.linkedin.com/in/pablo-pallitto\n\n"
            "Teléfono: +54 9 11 2251-2731\n\n"
            "Estoy disponible para proyectos, consultas y colaboraciones."
        )
    else:
        texto = "Opción no reconocida."

    query.edit_message_text(text=texto, parse_mode='Markdown')

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(button_handler))

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
