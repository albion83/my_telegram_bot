from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, filters, CommandHandler, ContextTypes

# Definición de estados para el formulario
GET_NAME, GET_EMAIL, GET_CHALLENGE = range(3)
END = -1

async def start_contact_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Punto de entrada. Inicia el formulario y pide el nombre."""
    await update.message.reply_text("¡Excelente! Vamos a comenzar con tu solicitud. ¿Cuál es tu nombre?", reply_markup=ReplyKeyboardRemove())
    return GET_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura el nombre y pide el email."""
    context.user_data['name'] = update.message.text
    await update.message.reply_text(f"Hola, {context.user_data['name']}. Ahora, ¿cuál es tu email para que pueda contactarte?")
    return GET_EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura el email y pide el desafío de negocio."""
    user_email = update.message.text
    if "@" not in user_email or "." not in user_email:
        await update.message.reply_text("Eso no parece un email válido. Intenta de nuevo:")
        return GET_EMAIL 

    context.user_data['email'] = user_email
    await update.message.reply_text("¡Listo! Para entender mejor, ¿cuál es el desafío principal que quieres resolver con la consultoría?")
    return GET_CHALLENGE

async def get_challenge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura el desafío y finaliza el formulario."""
    context.user_data['challenge'] = update.message.text
    
    summary = (
        f"✅ **Solicitud de Consultoría Recibida**\n"
        f"👤 Nombre: {context.user_data.get('name', 'N/A')}\n"
        f"📧 Email: {context.user_data.get('email', 'N/A')}\n"
        f"📝 Desafío: {context.user_data['challenge']}"
    )
    
    await update.message.reply_markdown(summary)
    await update.message.reply_text(
        "¡Gracias! He recibido tu solicitud. Te contactaré a la brevedad para discutir los detalles."
    )
    
    return END

async def cancel_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela el formulario."""
    await update.message.reply_text("Formulario de contacto cancelado. ¡Cuando quieras, usa /start para comenzar de nuevo!")
    context.user_data.clear()
    return END

# CONVERSATION HANDLER EXPORTADO
# El entry point se define como un MessageHandler para iniciar desde un botón de texto
contact_form_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^(✉️ Solicitar Consultoría)$"), start_contact_form)], 
    states={
        GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        GET_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
        GET_CHALLENGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_challenge)],
    },
    fallbacks=[CommandHandler("cancelar", cancel_form)],
    map_to_parent={END: ConversationHandler.END}
)