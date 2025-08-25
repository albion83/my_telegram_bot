import os
import logging
from dotenv import load_dotenv 
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove # <-- NUEVA IMPORTACIÓN
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler,
)
from simulated_data import get_jira_status

# --- 1. CONFIGURACIÓN ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Definición de estados para el formulario
GET_NAME, GET_EMAIL, GET_CHALLENGE = range(3)

# --- 2. HANDLERS DE COMANDOS Y MENÚ ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde al comando /start con un saludo y el menú principal."""
    user = update.effective_user.first_name if update.effective_user else "Estimado Usuario"
    
    keyboard = [
        [KeyboardButton("📊 Análisis de Datos")],
        [KeyboardButton("⚙️ Admin. de Plataformas")],
        [KeyboardButton("✉️ Solicitar Consultoría")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    welcome_message = (
        f"¡Hola {user}! Soy tu Asistente de Consultoría en Data y Gestión.\n\n"
        "Selecciona una opción para comenzar a explorar mis servicios y experiencia."
    )
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# --- 3. HANDLERS DEL FORMULARIO DE CONTACTO (ConversationHandler) ---

async def start_contact_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Punto de entrada. Inicia el formulario y pide el nombre."""
    # Opcional: Remover teclado si se usa el botón.
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
    # Validación básica
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
    
    # Después de finalizar, volvemos a mostrar el menú principal
    await start_command(update, context) 

    context.user_data.clear()
    return ConversationHandler.END 

async def cancel_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela el formulario."""
    await update.message.reply_text("Formulario de contacto cancelado. ¡Cuando quieras, usa /start para comenzar de nuevo!")
    context.user_data.clear()
    return ConversationHandler.END 

# --- 4. HANDLER PARA MENSAJES DE TEXTO ---

async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja los mensajes de texto, incluyendo botones y la consulta de tickets."""
    text = update.message.text

    if text == "📊 Análisis de Datos":
        response = (
            "Módulo de Análisis de Datos seleccionado.\n\n"
            "Mis herramientas clave: **Power BI**, **Excel** (avanzado), **SQL** y **Python**.\n\n"
            "Pronto: Podrás probar mi simulador de consultas SQL/Python."
        )
        await update.message.reply_text(response)
        # Volvemos al menú principal
        await start_command(update, context) 
        return
        
    elif text == "⚙️ Admin. de Plataformas":
        # QUITAMOS el menú de botones para que el usuario pueda escribir el ID
        await update.message.reply_text(
            "Módulo de Administración seleccionado. ¡Aquí demuestro mi dominio en las APIs de Jira, HubSpot y Teamwork!\n\n"
            "Ingresa un ID de ticket de prueba (ej: **DATABOT-101** o **JIRA-205**) para consultar su estado simulado.",
            reply_markup=ReplyKeyboardRemove() # <--- Oculta el teclado
        )
        return

    # LÓGICA DE CONSULTA DE TICKET SIMULADO
    if len(text) <= 15 and '-' in text and not text.startswith('/'):
        ticket_info = get_jira_status(text)
        
        if ticket_info:
            response = (
                f"✅ **Ticket Simulador Encontrado (Demo Jira)**\n"
                f"ID: `{ticket_info['ticket_id']}`\n"
                f"Resumen: {ticket_info['summary']}\n"
                f"Estado: **{ticket_info['status']}**\n"
                f"Prioridad: {ticket_info['priority']}\n"
                f"Asignado: {ticket_info['assigned_to']}"
            )
            await update.message.reply_markdown(response)
        else:
            response = f"Ticket ID '{text}' no encontrado en la base de datos simulada."
            await update.message.reply_text(response)
        
        # Después de la consulta, volvemos a mostrar el menú principal
        await start_command(update, context) 
        return

    # RESPUESTA POR DEFECTO
    await update.message.reply_text("Lo siento, no entendí ese mensaje. Usa /start para ver el menú principal.")

# --- 5. FUNCIÓN PRINCIPAL (MAIN) ---

def main() -> None:
    """Configura y ejecuta el bot."""
    
    load_dotenv() 
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("\nERROR CRÍTICO: La variable de entorno TELEGRAM_BOT_TOKEN no se encontró.")
        return

    application = Application.builder().token(token).build() 

    # Handler para el comando /start
    application.add_handler(CommandHandler("start", start_command))
    
    # Handler para el formulario de contacto (ConversationHandler)
    contact_handler = ConversationHandler(
        # Inicia la conversación cuando el usuario hace click en el botón
        entry_points=[MessageHandler(filters.Regex("^(✉️ Solicitar Consultoría)$"), start_contact_form)], 
        states={
            GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            GET_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            GET_CHALLENGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_challenge)],
        },
        # Comando para salir del formulario en cualquier momento
        fallbacks=[CommandHandler("cancelar", cancel_form)], 
    )

    application.add_handler(contact_handler)

    # Handler de mensajes de texto (para los demás botones y tickets)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))

    print("Bot Iniciado. Buscando actualizaciones... (Ctrl+C para detener)")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()