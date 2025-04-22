import os
import openpyxl
from docx import Document
import zipfile
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

# --- Vérification de l'existence du fichier RPO ---
if os.path.exists(EXCEL_FILE_PATH):
    print(f"Le fichier RPO existe et sera ajouté au ZIP à {EXCEL_FILE_PATH}")
else:
    print(f"Erreur : Le fichier RPO n'a pas été généré.")

# --- Créer le fichier ZIP ---
zip_file = os.path.join(output_directory, "pack_fiches_rpo.zip")  # Crée le chemin complet du ZIP
print(f"Création du fichier ZIP à : {zip_file}")

with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Ajouter le fichier RPO au ZIP
    if os.path.exists(EXCEL_FILE_PATH):
        zipf.write(EXCEL_FILE_PATH, os.path.basename(EXCEL_FILE_PATH))
        print(f"Le fichier RPO a été ajouté au ZIP : {EXCEL_FILE_PATH}")
    else:
        print(f"Erreur : Le fichier RPO n'existe pas.")

    # Générer et ajouter les fiches de poste et les mails
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if len(row) < 6:
            continue

        # Création des données pour chaque fiche de poste et mail type
        data = {
            "Nom du client": row[4] if len(row) > 4 else "",
            "Secteur d'activité": row[3] if len(row) > 3 else "Non précisé",
            "Localisation": row[5] if len(row) > 5 else "",
            "Titre du poste recherché": row[6] if len(row) > 6 else "",
            "Statut": row[7] if len(row) > 7 else "",
            "Nombre d'années d'expérience": row[8] if len(row) > 8 else "",
            "Date de démarrage": row[10] if len(row) > 10 else "",
            "TJM": row[11] if len(row) > 11 else "",
            "Salaire": row[12] if len(row) > 12 else "",
            "Télétravail": row[13] if len(row) > 13 else "",
            "Durée de la mission": row[14] if len(row) > 14 else "",
            "Projet": row[15] if len(row) > 15 else "",
            "Compétences obligatoires": row[16] if len(row) > 16 else "",
            "Taille de l'équipe": row[17] if len(row) > 17 else ""
        }

        #
