import openai
import streamlit as st
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from docx import Document
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API OpenAI depuis le fichier .env
API_KEY = os.getenv("OPENAI_API_KEY")

# Vérifier si la clé API a été correctement chargée
if not API_KEY:
    st.error("La clé API OpenAI est manquante. Assurez-vous qu'elle est dans le fichier .env.")
else:
    openai.api_key = API_KEY

# --- Fonction pour récupérer les données de Google Sheets ---
SERVICE_ACCOUNT_FILE = '/Users/ahmeddiomande/Documents/IDEALMATCH2025/generateur-fiches-clean/.devcontainer/peak-dominion-453716-v3-502cdb22fa02.json'
FOLDER_ID = '19uTtwgjpK4tYjcENCSDbpLCtAgK_sGkW'  # ID de ton dossier Google Drive

# Créer les identifiants d'authentification pour l'API Google Sheets
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])

# Construire le service pour l'API Google Sheets
service = build('sheets', 'v4', credentials=credentials)

SPREADSHEET_ID = '1wl_OvLv7c8iN8Z40Xutu7CyrN9rTIQeKgpkDJFtyKIU'  # ID de ton fichier Google Sheets
RANGE_NAME = 'Besoins ASI!A1:Z1000'  # Plage des données

# Fonction pour récupérer les données depuis la feuille de calcul
def recuperer_donnees_google_sheet():
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    return values

# --- Fonction pour générer la fiche de poste dans Google Drive ---
def enregistrer_fiche_google_drive(nom_fichier, contenu_fiche):
    doc = Document()
    doc.add_heading(f'Fiche de Poste : {nom_fichier}', 0)
    doc.add_paragraph(contenu_fiche)
    
    file_path = f'/content/drive/My Drive/{FOLDER_ID}/{nom_fichier}.docx'
    doc.save(file_path)
    return file_path

# --- Création des fiches de poste à partir du fichier RPO ---
if st.button('Générer à partir du fichier RPO'):
    # Récupérer les données du fichier RPO
    donnees_rpo = recuperer_donnees_google_sheet()

    for ligne in donnees_rpo[1:]:  # Ignorer la première ligne (en-têtes)
        poste_selectionne = dict(zip(donnees_rpo[0], ligne))  # Associer les colonnes aux valeurs de la ligne

        # Vérifier et remplacer la "Durée de la mission" si manquante
        duree_mission = poste_selectionne.get('Durée de la mission', '6 mois')  # 6 mois par défaut si absent

        # Créer le prompt pour OpenAI avec les données récupérées
        prompt_rpo = f"""
        Générer une fiche de poste pour le poste {poste_selectionne['Titre du poste recherché']} en utilisant les informations suivantes :
        - Durée de la mission : {duree_mission}
        - Statut mission : {poste_selectionne['statut mission']}
        - Compétences obligatoires : {poste_selectionne['Compétences obligatoires ( Préciser technologies principales et frameworks pour les postes techniques )']}
        - Projet : {poste_selectionne['Projet sur lequel va travailler le ou la candidate :']}
        - Localisation : {poste_selectionne['Localisation']}
        """

        try:
            # Appeler l'API OpenAI avec le prompt généré (correctement avec ChatCompletion)
            response_rpo = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Ou gpt-4 si tu l'as
                messages=[
                    {"role": "system", "content": "Vous êtes un assistant utile qui génère des fiches de poste."},
                    {"role": "user", "content": prompt_rpo}
                ],
                max_tokens=500
            )

            # Sauvegarder la fiche de poste dans Google Drive
            contenu_fiche = response_rpo.choices[0].message['content'].strip()
            nom_fichier = f"Fiche_{poste_selectionne['Titre du poste recherché']}"
            lien_drive = enregistrer_fiche_google_drive(nom_fichier, contenu_fiche)

            st.subheader(f"Fiche de Poste générée pour : {poste_selectionne['Titre du poste recherché']}")
            st.write(contenu_fiche)
            st.write(f"Fiche stockée sur Google Drive : {lien_drive}")

        except Exception as e:
            st.error(f"Erreur lors de la génération de la fiche de poste pour {poste_selectionne['Titre du poste recherché']}: {e}")
