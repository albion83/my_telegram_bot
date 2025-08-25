import os
import logging
from dotenv import load_dotenv 
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, ContextTypes, MessageHandler, filters, CommandHandler, ConversationHandler

# --- IMPORTACIONES DE MÓDULOS ---
# Importa los ConversationHandlers completos desde los otros archivos
from contact_form import contact_form_handler
from cv_handler import cv_conversation_handler

# Importar el handler de tickets simulados (asume que simulated_data.py existe)
from simulated_data import get_jira_status

# --- 1. CONFIGURACIÓN ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- 2. HANDLERS DE COMANDOS Y MENÚ ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde al comando /start con un saludo y el menú principal."""
    user = update.effective_user.first_name if update.effective_user else "Estimado Usuario"
    
    keyboard = [
        [KeyboardButton("📊 Análisis de Datos"), KeyboardButton("⚙️ Admin. de Plataformas")],
        [KeyboardButton("✉️ Solicitar Consultoría"), KeyboardButton("📄 Explorar mi CV")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    welcome_message = (
        f"¡Hola {user}! Soy tu Asistente de Consultoría en Data y Gestión.\n\n"
        "Selecciona una opción para comenzar a explorar mis servicios y experiencia."
    )
    
    if update.message:
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_message, reply_markup=reply_markup)

# --- 3. HANDLER PARA MENSAJES DE TEXTO (maneja lógicas secundarias y tickets) ---

async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Maneja los mensajes de texto que no son parte de una conversación activa."""
    text = update.message.text

    if text == "📊 Análisis de Datos":
        response = "Módulo de Análisis de Datos seleccionado.\n\nMis herramientas clave: **Power BI**, **Excel** (avanzado), **SQL** y **Python**."
        await update.message.reply_text(response)
        return ConversationHandler.END 
        
    elif text == "⚙️ Admin. de Plataformas":
        await update.message.reply_text(
            "Módulo de Administración seleccionado. ¡Aquí demuestro mi dominio en las APIs de Jira, HubSpot y Teamwork!\n\nIngresa un ID de ticket de prueba (ej: **DATABOT-101** o **JIRA-205**) para consultar su estado simulado."
        )
        return ConversationHandler.END

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
        
        return ConversationHandler.END

    await update.message.reply_text("Lo siento, no entendí ese mensaje. Usa /start para ver el menú principal.")
    return ConversationHandler.END

# --- 4. FUNCIÓN PRINCIPAL (MAIN) ---

def main() -> None:
    """Configura y ejecuta el bot."""
    
    load_dotenv() 
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("\nERROR CRÍTICO: La variable de entorno TELEGRAM_BOT_TOKEN no se encontró.")
        return

    application = Application.builder().token(token).build() 

    # Añadir handlers a la aplicación. Ya vienen configurados desde sus módulos.
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(contact_form_handler)
    application.add_handler(cv_conversation_handler)

    # Este manejador debe ir al final, para capturar mensajes que no inician o siguen una conversación
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))

    print("Bot Iniciado. Buscando actualizaciones... (Ctrl+C para detener)")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()