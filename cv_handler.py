from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Definición de estados para el CV Conversacional
CV_MENU, EXPERIENCE, SKILLS, EDUCATION, CONTACT = range(5)
END = -1

async def start_cv_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Punto de entrada. Muestra el menú principal del CV."""
    keyboard = [
        [InlineKeyboardButton("🚀 Trayectoria y Logros", callback_data="cv_exp")],
        [InlineKeyboardButton("🧠 Stack Tecnológico", callback_data="cv_skills")],
        [InlineKeyboardButton("🎓 Formación", callback_data="cv_edu")],
        [InlineKeyboardButton("💬 Contacto Directo", callback_data="cv_contact")],
        [InlineKeyboardButton("⬅️ Volver al Menú Principal", callback_data="cv_exit")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            "¡Bienvenido a mi perfil interactivo! 👋 ¿Qué área de mi experiencia profesional le gustaría profundizar?", 
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "¡Bienvenido a mi perfil interactivo! 👋 ¿Qué área de mi experiencia profesional le gustaría profundizar?", 
            reply_markup=reply_markup
        )
    return CV_MENU

async def cv_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Maneja la selección del menú del CV."""
    query = update.callback_query
    await query.answer()

    if query.data == "cv_exp":
        await query.edit_message_text(
            text=("🚀 **Trayectoria: Consultoría y Optimización de Procesos**\n\n"
                  "**01/2023 - Hoy | Analista de Procesos y Herramientas**\n"
                  "📈 **Impacto en el Negocio:** Liderazgo en el **diseño y automatización** de procesos que resultaron en una mejora de la **eficiencia operativa**.\n"
                  "💡 **Innovación:** Implementación estratégica de soluciones de **Business Intelligence (BI)**, transformando datos brutos en inteligencia de negocio.\n"
                  "🔗 **Coordinación:** Gestión y optimización avanzada de plataformas **Jira y Confluence** para asegurar la trazabilidad y la entrega puntual de proyectos.\n\n"
                  "**2018 - 2022 | Soporte y Monitoreo Estratégico**\n"
                  "🛡️ **Resiliencia:** Experticia en **Nagios y Pandora FMS** para garantizar un **uptime** cercano al 100% de la infraestructura crítica.\n"
                  "☁️ **Arquitectura:** Configuración y optimización de **servidores Linux**, reduciendo la latencia y los costos de mantenimiento."),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Volver al Menú CV", callback_data="cv_back")]])
        )
        return EXPERIENCE

    elif query.data == "cv_skills":
        await query.edit_message_text(
            text=("🧠 **Stack Tecnológico: El Conjunto de Herramientas del Consultor**\n\n"
                  "**ANÁLISIS Y PYTHON:** \n"
                  "• **Python:** Desarrollo de scripts para ETL, automatización de tareas y análisis predictivo inicial.\n"
                  "• **SQL:** Consultas complejas y diseño de modelos de datos para reporting.\n\n"
                  "**VISUALIZACIÓN Y BI:** \n"
                  "• **Power BI / Power Platform:** Creación de paneles dinámicos y soluciones de BI *end-to-end* para ejecutivos.\n\n"
                  "**PLATAFORMAS Y FLUJOS DE TRABAJO:** \n"
                  "• **Jira (Admin):** Configuración de flujos de trabajo personalizados y automatizaciones que optimizan el ciclo de vida del ticket.\n"
                  "• **Office 365** (0365): Integración de ecosistemas de trabajo colaborativo.\n\n"
                  "**COMPETENCIAS CLAVE:** **Orientación a Resultados**, Comunicación de Impacto (traducir lo técnico a lenguaje de negocio) y Planificación Rigurosa."),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Volver al Menú CV", callback_data="cv_back")]])
        )
        return SKILLS
        
    elif query.data == "cv_edu":
        await query.edit_message_text(
            text=("🎓 **Formación Académica: La Base Analítica y Técnica**\n\n"
                  "Mi educación formal respalda mi capacidad para abordar desafíos de sistemas complejos y análisis de datos.\n\n"
                  "**Técnico Superior en Análisis de Sistemas** (IFTS N° 12, 2015-2016).\n"
                  "**Técnico en Computación** (Hogar Naval Stella Maris N°37 D.E. N°11, 1996-2001).\n\n"
                  "Me especializo en la **intersección entre IT y Estrategia de Negocio**."),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Volver al Menú CV", callback_data="cv_back")]])
        )
        return EDUCATION

    elif query.data == "cv_contact":
        await query.edit_message_text(
            text=("💬 **¡Conectemos! Hablemos de su próximo proyecto:**\n\n"
                  "Si mi experiencia en optimización, BI y gestión de plataformas se alinea con sus necesidades, no dude en contactarme. Estoy listo para discutir cómo puedo aportar valor a su equipo.\n\n"
                  "📧 **Email:** pablo.pallitto@gmail.com\n"
                  "📞 **Teléfono:** (54) 9 11 2251-2731\n"
                  "🔗 **LinkedIn:** www.linkedin.com/in/pablo-pallitto\n"
                  "🌐 **Portafolio:** curriculumvitae.pablopallitto.ar"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Volver al Menú CV", callback_data="cv_back")]])
        )
        return CONTACT
    
    elif query.data == "cv_back":
        await start_cv_menu(update, context) 
        return CV_MENU

    elif query.data == "cv_exit":
        await query.edit_message_text(text="¡Gracias por tu interés en mi perfil! Volviendo al menú principal...")
        return END 

    return CV_MENU

# CONVERSATION HANDLER EXPORTADO
# El entry point se define como un MessageHandler para iniciar desde un botón de texto
cv_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^(📄 Explorar mi CV)$"), start_cv_menu)],
    states={
        CV_MENU: [CallbackQueryHandler(cv_menu_selection, pattern=r'cv_.*')],
        EXPERIENCE: [CallbackQueryHandler(cv_menu_selection, pattern=r'cv_.*')],
        SKILLS: [CallbackQueryHandler(cv_menu_selection, pattern=r'cv_.*')],
        EDUCATION: [CallbackQueryHandler(cv_menu_selection, pattern=r'cv_.*')],
        CONTACT: [CallbackQueryHandler(cv_menu_selection, pattern=r'cv_.*')]
    },
    fallbacks=[CallbackQueryHandler(cv_menu_selection, pattern="^cv_exit$")],
    map_to_parent={END: ConversationHandler.END}
)