import os
import logging
from dotenv import load_dotenv 
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from simulated_data import get_jira_status # <--- ¡Importación de la función de consulta!

# Configuración básica del logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- 1. DEFINICIÓN DE HANDLERS (Funciones que responden) ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde al comando /start con un saludo y el menú principal."""
    user = update.effective_user.first_name if update.effective_user else "Estimado Usuario"
    
    # Define los botones del menú 
    keyboard = [
        [KeyboardButton("📊 Análisis de Datos")],
        [KeyboardButton("⚙️ Admin. de Plataformas")],
        [KeyboardButton("✉️ Solicitar Consultoría (/contacto)")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    welcome_message = (
        f"¡Hola {user}! Soy tu Asistente de Consultoría en Data y Gestión.\n\n"
        "Selecciona una opción para comenzar a explorar mis servicios y experiencia."
    )
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def contacto_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Información de contacto."""
    message = (
        "¡Excelente! Para una consulta detallada, contáctame directamente.\n\n"
        "🔗 **LinkedIn:** [Pega tu Enlace de LinkedIn aquí]\n"
        "📧 **Email:** tu.email@ejemplo.com\n\n"
        "*(Pronto implementaremos un formulario guiado aquí para capturar tu solicitud)*"
    )
    await update.message.reply_text(message)

async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja los mensajes de texto, incluyendo botones y la consulta de tickets."""
    text = update.message.text
    
    # --- 1. LÓGICA DE RESPUESTA A BOTONES ---
    if text == "📊 Análisis de Datos":
        response = (
            "Módulo de Análisis de Datos seleccionado.\n\n"
            "Mis herramientas clave: **Power BI**, **Excel** (avanzado), **SQL** y **Python**.\n\n"
            "Pronto: Podrás probar mi simulador de consultas SQL/Python."
        )
        await update.message.reply_text(response)
        return
        
    elif text == "⚙️ Admin. de Plataformas":
        # Respuesta que solicita el ID de ticket
        await update.message.reply_text(
            "Módulo de Administración seleccionado. ¡Aquí demuestro mi dominio en las APIs de Jira, HubSpot y Teamwork!\n\n"
            "Ingresa un ID de ticket de prueba (ej: **DATABOT-101** o **JIRA-205**) para consultar su estado simulado."
        )
        return

    elif "Solicitar Consultoría" in text:
        await contacto_command(update, context)
        return

    # --- 2. LÓGICA DE CONSULTA DE TICKET SIMULADO (Fase 2) ---
    # Patrón: Contiene un '-' (guion), no es demasiado largo (<=15 caracteres), y no empieza por '/' (comando).
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
            return
        else:
            response = f"Ticket ID '{text}' no encontrado en la base de datos simulada."
            await update.message.reply_text(response)
            return

    # --- 3. RESPUESTA POR DEFECTO ---
    await update.message.reply_text("Lo siento, no entendí ese mensaje. Usa /start para ver el menú principal.")


# --- 4. FUNCIÓN PRINCIPAL (MAIN) ---

def main() -> None:
    """Configura y ejecuta el bot."""
    
    # 1. Carga las variables de entorno desde el archivo .env
    load_dotenv() 
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("\nERROR CRÍTICO: La variable de entorno TELEGRAM_BOT_TOKEN no se encontró.")
        print("Asegúrate de haber creado el archivo .env y haber pegado el token ahí.")
        return

    # 2. Crea la aplicación
    application = Application.builder().token(token).build() 

    # 3. Asocia los handlers (Comandos y Mensajes)
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("contacto", contacto_command))
    
    # Escucha cualquier mensaje de texto que NO sea un comando (/start, /contacto, etc.)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))

    # 4. Inicia el bot
    print("Bot Iniciado. Buscando actualizaciones... (Ctrl+C para detener)")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()