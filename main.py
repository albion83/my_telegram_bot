import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters, ConversationHandler
)
from google_sheets import save_interaction
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ No se encontró el token de Telegram. Definí BOT_TOKEN en el entorno o en .env.")

# Estados para el ConversationHandler
ESPERANDO_CONTACTO = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "¡Hola! 👋\n"
        "Soy el bot de Pablo Pallitto. Podés consultarme sobre mi experiencia, ver mi portfolio o dejarme tu contacto.\n\n"
        "📬 Elegí una opción o escribime un mensaje directamente."
    )

    keyboard = [
        [InlineKeyboardButton("📄 Ver experiencia", callback_data="experiencia")],
        [InlineKeyboardButton("🖼️ Ver portfolio", callback_data="portfolio")],
        [InlineKeyboardButton("📬 Dejar contacto", callback_data="contacto")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(msg, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "experiencia":
        await query.edit_message_text(
            "📄 Pablo tiene experiencia en análisis de datos, desarrollo en Power BI y automatización de procesos con Power Platform.\n\n"
            "Volvé al menú con /start"
        )
    elif query.data == "portfolio":
        await query.edit_message_text(
            "🖼️ Podés ver el portfolio completo de Pablo en: https://tulink.com\n\n"
            "Volvé al menú con /start"
        )
    elif query.data == "contacto":
        await query.edit_message_text("✍️ Por favor, escribime tu nombre, email y mensaje para dejar tu contacto.")
        return ESPERANDO_CONTACTO  # Cambio de estado para esperar el mensaje

    return ConversationHandler.END

async def recibir_contacto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    mensaje = update.message.text

    save_interaction(
        nombre=user.full_name,
        username=user.username,
        user_id=user.id,
        mensaje=mensaje
    )

    await update.message.reply_text("✅ ¡Gracias! Tu mensaje fue guardado. Volvé al menú con /start")

    return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Mensaje general fuera de conversación
    user = update.effective_user
    mensaje = update.message.text

    save_interaction(
        nombre=user.full_name,
        username=user.username,
        user_id=user.id,
        mensaje=mensaje
    )

    await update.message.reply_text("✅ ¡Gracias! Tu mensaje fue guardado.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operación cancelada. Volvé al menú con /start")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler)],
        states={
            ESPERANDO_CONTACTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_contacto)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
