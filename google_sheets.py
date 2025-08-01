import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Autenticación con Google Sheets
def connect_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("TelegramBot_Interacciones").worksheet("interacciones")
    return sheet

# Guardar interacción en la hoja
def save_interaction(nombre, username, user_id, mensaje):
    sheet = connect_sheet()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, nombre, username, user_id, mensaje])
