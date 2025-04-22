import os
import openpyxl
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Charger la clé API OpenAI
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# --- Créer le répertoire output/ si nécessaire ---
output_directory = "output"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    print(f"Répertoire {output_directory} créé.")
else:
    print(f"Le répertoire {output_directory} existe déjà.")

# --- Création du fichier Excel RPO ---
EXCEL_FILE_PATH = os.path.join(output_directory, 'RPO.xlsx')

# --- Authentification Google Sheets ---
SERVICE_ACCOUNT_FILE = './API/peak-dominion-453716-v3-502cdb22fa02.json'
SPREADSHEET_ID = '1wl_OvLv7c8iN8Z40Xutu7CyrN9rTIQeKgpkDJFtyKIU'
RANGE_NAME = 'Besoins ASI!A1:Z1000'

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
service = build('sheets', 'v4', credentials=credentials)

# Télécharger les données de Google Sheets
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

if not values:
    print("Aucune donnée trouvée dans le Google Sheets.")
else:
    print(f"{len(values)} lignes de données récupérées depuis Google Sheets.")

# Créer un fichier Excel avec les données récupérées
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Feuil1"
for row in values:
    ws.append(row)

wb.save(EXCEL_FILE_PATH)
print(f"Le fichier RPO a été créé et sauvegardé à : {EXCEL_FILE_PATH}")

# --- Lire le fichier Excel et l'afficher dans Streamlit ---
# Nous allons maintenant lire le fichier Excel et l'afficher dans Streamlit
try:
    df = pd.read_excel(EXCEL_FILE_PATH)
    print(f"Affichage des données de {EXCEL_FILE_PATH} dans Streamlit")
    
    # Si tout va bien, afficher les données dans Streamlit
    import streamlit as st
    st.title("Affichage des Données RPO")
    st.write("Voici les données extraites du fichier RPO :")
    st.dataframe(df)  # Affiche les données du fichier Excel dans Streamlit

except Exception as e:
    print(f"Erreur lors de la lecture ou de l'affichage du fichier RPO : {e}")
    import streamlit as st
    st.error(f"Erreur lors de l'affichage des données : {e}")
