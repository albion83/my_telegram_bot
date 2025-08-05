from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📞 Podés contactarme en: contacto@tucorreo.com")

handler = CommandHandler("contacto", contact_command)
