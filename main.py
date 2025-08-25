import os
import logging
from dotenv import load_dotenv 
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from simulated_data import get_jira_status

# Configuración básica del logging para ver errores en la terminal
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
    # resize_keyboard=True ajusta el tamaño, one_time_keyboard=False lo mantiene
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    welcome_message = (
        f"¡Hola {user}! Soy tu Asistente de Consultoría en Data y Gestión.\n\n"
        "Selecciona una opción para comenzar a explorar mis servicios y experiencia."
    )
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def contacto_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Información de contacto (o inicio del formulario de leads)."""
    message = (
        "¡Excelente! Para una consulta detallada, contáctame directamente.\n\n"
        "🔗 **LinkedIn:** [Pega tu Enlace de LinkedIn aquí]\n"
        "📧 **Email:** tu.email@ejemplo.com\n\n"
        "*(Pronto implementaremos un formulario guiado aquí para capturar tu solicitud)*"
    )
    await update.message.reply_text(message)

async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja los mensajes de texto que no son comandos, incluyendo los de los botones."""
    text = update.message.text
    response = ""
    
    if text == "📊 Análisis de Datos":
        response = (
            "Módulo de Análisis de Datos seleccionado.\n\n"
            "Mis herramientas clave: **Power BI**, **Excel** (avanzado), **SQL** y **Python**.\n\n"
            "Pronto: Podrás probar mi simulador de consultas SQL/Python."
        )
    elif text == "⚙️ Admin. de Plataformas":
        response = (
            "Módulo de Administración seleccionado.\n\n"
            "Mis herramientas clave: **Jira**, **HubSpot**, **Teamwork** y sus APIs.\n\n"
            "Pronto: Podrás consultar el estado de tickets/contactos simulados."
        )
    elif "Solicitar Consultoría" in text:
        # Si hacen clic en el botón de contacto, llamamos a la función
        await contacto_command(update, context)
        return
    else:
        # Respuesta por defecto para texto que no se reconoce
        response = "Lo siento, no entendí ese mensaje. Usa /start para ver el menú principal."

    await update.message.reply_text(response)


# --- 2. FUNCIÓN PRINCIPAL (MAIN) ---

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

    # 4. Inicia el bot (Modo Long Polling para desarrollo local)
    print("Bot Iniciado. Buscando actualizaciones... (Ctrl+C para detener)")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()