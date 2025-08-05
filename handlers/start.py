from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("📄 CV", callback_data='cv')],
        [InlineKeyboardButton("📞 Contacto", callback_data='contacto')],
        [InlineKeyboardButton("💼 Habilidades", callback_data='skills')],
        [InlineKeyboardButton("📝 Experiencia", callback_data='experiencia')],
        [InlineKeyboardButton("🎓 Formación", callback_data='formacion')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("👋 ¡Hola! Elegí una opción:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text("👋 ¡Hola! Elegí una opción:", reply_markup=reply_markup)
