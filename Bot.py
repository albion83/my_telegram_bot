import os
import asyncio
import threading
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
from dotenv import load_dotenv

# --- Cargar variables de entorno ---
load_dotenv()
TOKEN = os.getenv("TOKEN")
assert TOKEN, "❌ No se encontró el TOKEN en las variables de entorno."

# --- Instancias principales ---
app = Flask(__name__)
application = Application.builder().token(TOKEN).build()
WEBHOOK_PATH = f"/webhook/{TOKEN}"

# --- Comando /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await update.message.reply_text(text=mensaje, reply_markup=InlineKeyboardMarkup(botones))

# --- Manejo de botones ---
async def manejar_botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

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
        await query.edit_message_text(text=mensaje, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(botones_info))

    elif data == "cv_web":
        await query.edit_message_text(
            text="🌐 Podés ver mi CV online en:\nhttps://curriculumvitae.pablopallitto.ar",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬇️ Descargar CV PDF", callback_data="cv_pdf")],
                [InlineKeyboardButton("🔙 Volver al menú", callback_data="start")]
            ])
        )

    elif data == "cv_pdf":
        file_path = "CV_Pablo Norberto Pallitto Gomez.pdf"
        chat_id = query.message.chat.id
        try:
            with open(file_path, 'rb') as documento:
                await context.bot.send_document(chat_id=chat_id, document=documento, filename="CV_Pablo Norberto Pallitto Gomez.pdf")
            await query.edit_message_text(
                text="📄 Aquí tenés mi CV en PDF.\n\n¿Querés volver al menú?",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Volver al menú", callback_data="start")]
                ])
            )
        except FileNotFoundError:
            await query.edit_message_text("❌ No se encontró el archivo del CV. Por favor, intentá más tarde.")

    elif data == "servicios":
        mensaje = (
            "💼 *Servicios*\n"
            "- Análisis de datos y visualización\n"
            "- Creación de dashboards interactivos\n"
            "- Automatización de procesos con Python y Power BI\n"
            "- Consultoría para toma de decisiones basada en datos"
        )
        await query.edit_message_text(text=mensaje, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([
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
        await query.edit_message_text(text=mensaje, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Volver al menú", callback_data="start")]
        ]))

    elif data == "start":
        await start(update, context)

# --- Respuesta a mensajes ---
async def responder_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    respuestas = {
        "herramientas": "🛠️ Trabajo principalmente con Power BI, Python, SQL y Excel.",
        "experiencia": "📌 Tengo experiencia en análisis de datos para negocios, automatización de reportes y creación de dashboards para distintas industrias.",
        "trabajaste": "🏢 He colaborado con empresas de servicios, tecnología y retail. ¿Querés saber más sobre algún proyecto específico?",
        "proyectos": "🚀 Estoy disponible para nuevos proyectos. Si tenés algo en mente, ¡escribime!"
    }
    for keyword, respuesta in respuestas.items():
        if keyword in texto:
            await update.message.reply_text(respuesta)
            return
    await update.message.reply_text("🤖 No entiendo tu consulta. Por favor, usá los botones del menú o escribí /start para comenzar.")

# --- Añadir handlers ---
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(manejar_botones))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_texto))

# --- Ruta del webhook ---
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    update_data = request.get_json(force=True)
    update = Update.de_json(update_data, application.bot)
    await application.process_update(update)
    return "OK", 200

# --- Ruta raíz ---
@app.route("/", methods=["GET"])
def index():
    return "✅ Bot de Pablo está funcionando."

# --- Inicializar bot de Telegram ---
async def run_bot():
    await application.initialize()
    await application.start()
    print("🤖 Bot de Telegram inicializado y escuchando Webhook.")

# --- Ejecutar Flask y el bot ---
if __name__ == "__main__":
    threading.Thread(target=lambda: asyncio.run(run_bot()), daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
