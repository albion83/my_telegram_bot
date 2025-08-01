from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from google_sheets import save_interaction

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = (
        f"¡Hola {user.first_name}! 👋\n"
        "Soy el bot de Pablo Pallitto. Podés consultarme sobre mi experiencia, ver mi portfolio o dejarme tu contacto.\n\n"
        "📬 Enviame un mensaje y lo guardaré para que Pablo lo vea."
    )
    await update.message.reply_text(msg)

# Mensaje general → lo guarda en Google Sheets
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

# Iniciar el bot
if __name__ == '__main__':
    import os

    TOKEN = os.getenv("BOT_TOKEN")  # Puedes cargarlo desde .env o variable de entorno

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot corriendo...")
    app.run_polling()
