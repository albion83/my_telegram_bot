from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def experiencia_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texto = (
        "💼 Experiencia profesional:\n"
        "- Analista de Datos en Empresa X (2021 - Presente)\n"
        "- Desarrollador Python en Empresa Y (2019 - 2021)\n"
        "- Consultor Power BI Freelance (2018 - 2019)"
    )
    await update.message.reply_text(texto)

handler = CommandHandler("experiencia", experiencia_command)
