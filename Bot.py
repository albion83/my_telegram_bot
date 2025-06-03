from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

# Diccionario de respuestas automáticas
RESPUESTAS_FAQ = {
    "herramientas": "🔧 Uso herramientas como Power BI, Python, SQL, Excel y Google Data Studio.",
    "usas": "🔧 Uso herramientas como Power BI, Python, SQL, Excel y Google Data Studio.",
    "tecnología": "🔧 Uso herramientas como Power BI, Python, SQL, Excel y Google Data Studio.",
    "trabajaste": "💼 Tengo experiencia en proyectos freelance y trabajos con empresas de diversas industrias.",
    "experiencia": "💼 Tengo experiencia en proyectos freelance y trabajos con empresas de diversas industrias.",
    "proyectos": "📊 He desarrollado dashboards interactivos, automatizaciones con Python y análisis de datos para toma de decisiones.",
    "contacto": "📞 Podés contactarme por email: pablo.pallitto@gmail.com o LinkedIn: https://www.linkedin.com/in/pablo-pallitto",
}

# Comandos con botones
def start(update, context):
    nombre = update.effective_user.first_name
    mensaje = (
        f"Hola {nombre}, ¡bienvenido a Pablo Analytics Bot! 👋\n\n"
        "📊 Soy tu asistente personal para conocer más sobre mí, mis servicios en análisis de datos y cómo puedo ayudarte.\n\n"
        "Elegí una opción para comenzar:"
    )

    botones = [
        [InlineKeyboardButton("📄 Sobre mí", callback_data="info")],
        [InlineKeyboardButton("📂 Ver CV", callback_data="cv")],
        [InlineKeyboardButton("💼 Servicios", callback_data="servicios")],
        [InlineKeyboardButton("📞 Contacto", callback_data="contacto")]
    ]

    reply_markup = InlineKeyboardMarkup(botones)
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

# CallbackQuery para los botones
def manejar_botones(update, context):
    query = update.callback_query
    data = query.data
    query.answer()  # Para detener el "cargando..."

    if data == "info":
        info(update, context)
    elif data == "cv":
        cv(update, context)
    elif data == "servicios":
        servicios(update, context)
    elif data == "contacto":
        contacto(update, context)

# Respuestas automáticas por keywords
def respuestas_frecuentes(update, context):
    mensaje = update.message.text.lower()
    for palabra_clave, respuesta in RESPUESTAS_FAQ.items():
        if palabra_clave in mensaje:
            context.bot.send_message(chat_id=update.effective_chat.id, text=respuesta)
            return
    context.bot.send_message(chat_id=update.effective_chat.id, text="🤔 No entendí tu consulta. Probá con otra frase o usá el menú.")

# Handlers
from telegram.ext import CallbackQueryHandler
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("info", info))
dispatcher.add_handler(CommandHandler("cv", cv))
dispatcher.add_handler(CommandHandler("servicios", servicios))
dispatcher.add_handler(CommandHandler("contacto", contacto))
dispatcher.add_handler(CallbackQueryHandler(manejar_botones))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, respuestas_frecuentes))

# Webhook para Telegram
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# Ruta raíz
@app.route("/", methods=["GET"])
def index():
    return "Bot de Pablo está funcionando."

# Local
if __name__ == "__main__":
    app.run(debug=True)
