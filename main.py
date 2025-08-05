import os
import time
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)
from handlers import start, callbacks, cv

if os.path.exists(".env"):
    load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("No se encontró la variable de entorno BOT_TOKEN")

TIMEOUT = 600  # 10 minutos en segundos

async def check_inactivity(context: ContextTypes.DEFAULT_TYPE):
    current_time = time.time()
    users_to_remove = []
    for user_id, last_time in context.bot_data.get("last_active", {}).items():
        if current_time - last_time > TIMEOUT:
            users_to_remove.append(user_id)

    for user_id in users_to_remove:
        context.bot_data["last_active"].pop(user_id, None)
        # Opcional: enviar mensaje o hacer algo con user_id
        # await context.bot.send_message(chat_id=user_id, text="⏰ La conversación terminó por inactividad.")

async def update_user_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if "last_active" not in context.bot_data:
        context.bot_data["last_active"] = {}
    context.bot_data["last_active"][user_id] = time.time()

def main():
    application = Application.builder().token(TOKEN).build()

    # Handlers principales
    application.add_handler(CommandHandler("start", start.start_command))
    application.add_handler(CallbackQueryHandler(callbacks.button_handler))
    application.add_handler(CommandHandler("cv", cv.cv_command))  # comandos directos si quieres

    # Actualizar actividad del usuario en grupo 1 (prioridad menor)
    application.add_handler(CallbackQueryHandler(update_user_activity), group=1)
    application.add_handler(CommandHandler("start", update_user_activity), group=1)

    # Job que chequea inactividad cada minuto
    application.job_queue.run_repeating(check_inactivity, interval=60, first=60)

    print("✅ Bot iniciado correctamente. Esperando mensajes...")
    application.run_polling()

if __name__ == "__main__":
    main()
