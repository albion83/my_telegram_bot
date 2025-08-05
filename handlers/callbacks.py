from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data

    respuestas = {
        "cv": "📄 Aquí podés ver mi CV: https://tucv.com/mi-cv",
        "contacto": "📞 Podés contactarme en: contacto@tucorreo.com",
        "skills": "💼 Habilidades:\n- Python\n- Análisis de datos\n- Power BI\n- Automatización con APIs",
        "experiencia": (
            "💼 Experiencia profesional:\n"
            "- Analista de Datos en Empresa X (2021 - Presente)\n"
            "- Desarrollador Python en Empresa Y (2019 - 2021)\n"
            "- Consultor Power BI Freelance (2018 - 2019)"
        ),
        "formacion": (
            "🎓 Formación académica:\n"
            "- Licenciatura en Análisis de Datos - Universidad Z\n"
            "- Certificación Power BI - Microsoft\n"
            "- Cursos de Python avanzado y Machine Learning"
        ),
        "volver": None  # Especial para volver al menú
    }

    if data == "volver":
        # Mostramos menú otra vez
        keyboard = [
            [InlineKeyboardButton("📄 CV", callback_data='cv')],
            [InlineKeyboardButton("📞 Contacto", callback_data='contacto')],
            [InlineKeyboardButton("💼 Habilidades", callback_data='skills')],
            [InlineKeyboardButton("📝 Experiencia", callback_data='experiencia')],
            [InlineKeyboardButton("🎓 Formación", callback_data='formacion')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("👋 ¡Hola! Elegí una opción:", reply_markup=reply_markup)
        return

    texto = respuestas.get(data, "Opción no reconocida.")

    # Botón para volver al menú
    keyboard = [
        [InlineKeyboardButton("🔙 Volver al menú", callback_data='volver')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=texto, reply_markup=reply_markup)
