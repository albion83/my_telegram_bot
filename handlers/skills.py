from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def skills_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "💼 Mis habilidades incluyen:\n"
        "- Análisis de datos\n"
        "- Power BI\n"
        "- Python\n"
        "- Automatización con APIs\n"
    )

handler = CommandHandler("skills", skills_command)
