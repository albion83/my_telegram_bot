from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def cv_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📄 Aquí podés ver mi CV: https://tucv.com/mi-cv")

handler = CommandHandler("cv", cv_command)
