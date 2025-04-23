import openai
import streamlit as st
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import pandas as pd

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API OpenAI depuis le fichier .env
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

# --- Fonction pour récupérer les données depuis Google Sheets ---
SERVICE_ACCOUNT_FILE = '/Users/ahmeddiomande/Documents/IDEALMATCH2025/generateur-fiches-clean/.devcontainer/peak-dominion-453716-v3-502cdb22fa02.json'  # Chemin correct vers le fichier JSON
SPREADSHEET_ID = '1wl_OvLv7c8iN8Z40Xutu7CyrN9rTIQeKgpkDJFtyKIU'  # Remplacer par l'ID de ton fichier Google Sheets
RANGE_NAME = 'Besoins ASI!A1:Z1000'

def recuperer_donnees_google_sheet():
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    return values

# --- Interface Streamlit ---
st.title('🎯 IDEALMATCH JOB CREATOR')

# Zone de saisie du prompt utilisateur
user_prompt = st.text_area("Écrivez ici votre prompt pour générer une fiche de poste :", "Entrez ici le prompt pour ChatGPT...")

# Bouton pour générer à partir du fichier RPO
if st.button("Générer à partir du fichier RPO"):
    donnees_rpo = recuperer_donnees_google_sheet()
    if donnees_rpo:
        st.write("Données récupérées avec succès.")
        # Convertir les données en DataFrame pour un traitement facile
        df = pd.DataFrame(donnees_rpo[1:], columns=donnees_rpo[0])
        st.write(df)  # Affiche les premières lignes du fichier pour validation

        # Pour chaque ligne du DataFrame, générer une fiche de poste
        for _, row in df.iterrows():
            # Exemple d'utilisation du prompt pour chaque ligne
            prompt = user_prompt.format(**row.to_dict())
            try:
                # Appeler l'API OpenAI avec le prompt et générer une fiche de poste
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # Ou gpt-4 si tu l'as
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )

                # Afficher la fiche de poste générée
                fiche_poste = response.choices[0].message['content'].strip()
                st.subheader(f"Fiche de Poste pour {row['Titre du poste recherché']}")
                st.write(fiche_poste)

                # Sauvegarde sur Google Drive (mettre à jour avec ton code de sauvegarde sur Drive)
                # Exemple fictif :
                # with open(f"/content/drive/MyDrive/fiche_poste_{row['Titre du poste recherché']}.txt", "w") as f:
                #     f.write(fiche_poste)
            except Exception as e:
                st.error(f"Erreur lors de la génération de la fiche de poste : {e}")
    else:
        st.error("Erreur lors de la récupération des données depuis Google Sheets.")
