from flask import Flask, request, send_file
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
app = Flask(__name__)

dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

# Función para el comando /start
def start(update, context):
    nombre = update.effective_user.first_name
    mensaje = (
        f"Hola {nombre}, ¡bienvenido a Pablo Analytics Bot! 👋\n\n"
        "📊 Soy tu asistente personal para conocer más sobre mí, mis servicios en análisis de datos y cómo puedo ayudarte.\n\n"
        "Tocá los botones para navegar:"
    )

    botones = [
        [InlineKeyboardButton("👨‍💻 Sobre mí", callback_data="info")],
        [InlineKeyboardButton("💼 Servicios", callback_data="servicios")],
        [InlineKeyboardButton("📬 Contacto", callback_data="contacto")],
    ]

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=mensaje,
        reply_markup=InlineKeyboardMarkup(botones)
    )

# Función para manejar botones
def manejar_botones(update, context):
    query = update.callback_query
    data = query.data
    query.answer()

    if data == "info":
        mensaje = (
            "👨‍💻 *Sobre mí*\n"
            "Soy Pablo Norberto, especialista en análisis de datos con experiencia en proyectos de BI, dashboards y automatización.\n"
            "Me apasiona transformar datos en información clara y útil para la toma de decisiones.\n\n"
            "🧾 ¿Querés ver más sobre mi perfil?"
        )

        botones_info = [
            [InlineKeyboardButton("🌐 Ver CV Web", callback_data="cv_web")],
            [InlineKeyboardButton("⬇️ Descargar CV PDF", callback_data="cv_pdf")],
            [InlineKeyboardButton("🔙 Volver al menú", callback_data="start")]
        ]

        query.edit_message_text(
            text=mensaje,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(botones_info)
        )

    elif data == "cv_web":
        query.edit_message_text(
            text="🌐 Podés ver mi CV online en:\nhttps://curriculumvitae.pablopallitto.ar",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬇️ Descargar CV PDF", callback_data="cv_pdf")],
                [InlineKeyboardButton("🔙 Volver al menú", callback_data="start")]
            ])
        )

    elif data == "cv_pdf":
        file_path = "CV_Pablo Norberto Pallitto Gomez.pdf"
        chat_id = query.message.chat_id
        context.bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'), filename="CV_Pablo Norberto Pallitto Gomez.pdf")
        query.edit_message_text("📄 Aquí tenés mi CV en PDF.\n\n¿Querés volver al menú?", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver al menú", callback_data="start")]
        ]))

    elif data == "servicios":
        mensaje = (
            "💼 *Servicios*\n"
            "- Análisis de datos y visualización\n"
            "- Creación de dashboards interactivos\n"
            "- Automatización de procesos con Python y Power BI\n"
            "- Consultoría para toma de decisiones basada en datos"
        )

        query.edit_message_text(text=mensaje, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver al menú", callback_data="start")]
        ]))

    elif data == "contacto":
        mensaje = (
            "📞 *Contacto*\n"
            "Email: pablo.pallitto@gmail.com\n"
            "LinkedIn: https://www.linkedin.com/in/pablo-pallitto\n"
            "Teléfono: +54 9 11 2251-2731\n"
            "Estoy disponible para proyectos, consultas y colaboraciones."
        )

        query.edit_message_text(text=mensaje, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver al menú", callback_data="start")]
        ]))

    elif data == "start":
        start(update, context)

# Respuesta automática para preguntas frecuentes
def responder_texto(update, context):
    texto = update.message.text.lower()

    respuestas = {
        "herramientas": "🛠️ Trabajo principalmente con Power BI, Python, SQL y Excel.",
        "experiencia": "📌 Tengo experiencia en análisis de datos para negocios, automatización de reportes y creación de dashboards para distintas industrias.",
        "trabajaste": "🏢 He colaborado con empresas de servicios, tecnología y retail. ¿Querés saber más sobre algún proyecto específico?",
        "proyectos": "🚀 Estoy disponible para nuevos proyectos. Si tenés algo en mente, ¡escribime!"
    }

    for keyword, respuesta in respuestas.items():
        if keyword in texto:
            update.message.reply_text(respuesta)
            return

    update.message.reply_text("🤖 No entiendo tu consulta. Por favor, usá los botones del menú o escribí /start para comenzar.")

# Handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(manejar_botones))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_texto))

# Webhook para Telegram
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# Endpoint simple para probar
@app.route("/", methods=["GET"])
def index():
    return "Bot de Pablo está funcionando."

if __name__ == "__main__":
    app.run(debug=True)
