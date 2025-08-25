# simulated_data.py

# --- TABLA DE EJEMPLO DE JIRA ---
JIRA_TICKETS = [
    {
        "ticket_id": "DATABOT-101",
        "project_key": "DATABOT",
        "summary": "Configurar reporte de ventas en Power BI",
        "status": "EN PROGRESO",
        "priority": "Alta",
        "assigned_to": "Pablo"
    },
    {
        "ticket_id": "DATABOT-102",
        "project_key": "DATABOT",
        "summary": "Revisar flujo ETL de datos",
        "status": "HECHO",
        "priority": "Media",
        "assigned_to": "Pablo"
    },
    {
        "ticket_id": "JIRA-205",
        "project_key": "JIRA",
        "summary": "Creación de Dashboard de Gestión",
        "status": "TO DO",
        "priority": "Alta",
        "assigned_to": "Equipo Admin"
    },
]

def get_jira_status(ticket_id: str) -> dict | None:
    """Busca y retorna la información de un ticket simulado.

    Simula una consulta SQL o una llamada a la API buscando en la lista interna.
    """
    ticket_id = ticket_id.upper() # Normaliza el ID a mayúsculas
    
    for ticket in JIRA_TICKETS:
        if ticket["ticket_id"] == ticket_id:
            return ticket
    
    return None # Retorna None si no se encuentra