from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def formacion_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texto = (
        "🎓 Formación académica:\n"
        "- Licenciatura en Análisis de Datos - Universidad Z\n"
        "- Certificación Power BI - Microsoft\n"
        "- Cursos de Python avanzado y Machine Learning"
    )
    await update.message.reply_text(texto)

handler = CommandHandler("formacion", formacion_command)
