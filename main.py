import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
from google_sheets import save_interaction

# Cargar variables de entorno desde .env si existe
from dotenv import load_dotenv
load_dotenv()

# Obtener el token de entorno (local o de Render)
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ No se encontró el token de Telegram. Definí BOT_TOKEN en el entorno o en .env.")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = (
        f"¡Hola {user.first_name}! 👋\n"
        "Soy el bot de Pablo Pallitto. Podés consultarme sobre mi experiencia, ver mi portfolio o dejarme tu contacto.\n\n"
        "📬 Enviame un mensaje y lo guardaré para que Pablo lo vea."
    )
    await update.message.reply_text(msg)

# Mensajes generales
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    mensaje = update.message.text

    save_interaction(
        nombre=user.full_name,
        username=user.username,
        user_id=user.id,
        mensaje=mensaje
    )

    await update.message.reply_text("✅ ¡Gracias! Tu mensaje fue guardado.")

# Ejecutar bot
if __name__ == '__main__':
    print("🤖 Iniciando bot...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
