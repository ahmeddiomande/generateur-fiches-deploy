import openai
import streamlit as st
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
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

# --- Google Sheets API ---
SERVICE_ACCOUNT_FILE = '/Users/ahmeddiomande/Documents/IDEALMATCH2025/generateur-fiches-clean/.devcontainer/peak-dominion-453716-v3-502cdb22fa02.json'
SPREADSHEET_ID = '1wl_OvLv7c8iN8Z40Xutu7CyrN9rTIQeKgpkDJFtyKIU'  # ID du fichier Google Sheets
RANGE_NAME = 'Besoins ASI!A1:Z1000'  # Plage de données dans Google Sheets

# Créer les identifiants d'authentification pour l'API Google Sheets
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
service = build('sheets', 'v4', credentials=credentials)

# Fonction pour récupérer les données du fichier Google Sheets
def recuperer_donnees_google_sheet():
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    return values

# --- Mise en forme de l'interface Streamlit ---

# Titre principal
st.title('🎯 IDEALMATCH JOB CREATOR')

# Texte introductif
st.markdown("""
Bienvenue dans l'outil **IDEALMATCH JOB CREATOR** !  
Cet outil vous permet de générer des fiches de poste personnalisées à l'aide de l'intelligence artificielle (ChatGPT).

### Instructions :
- Entrez votre **prompt personnalisé** dans la zone de texte ci-dessous.
- Cliquez sur le bouton "Générer la Fiche de Poste" pour obtenir une fiche automatiquement générée.
- La fiche sera basée sur votre description du poste et des critères de sélection.

📝 **Astuces** :
- Soyez précis dans votre description pour obtenir les meilleurs résultats.
- L'outil utilise la dernière version de GPT-3.5 pour vous fournir des résultats de qualité.
""")

# --- Zone de saisie du prompt de l'utilisateur ---
user_prompt = st.text_area("Écrivez ici votre prompt pour générer une fiche de poste :", 
                          "Entrez ici le prompt pour ChatGPT...")

# --- Bouton pour envoyer la demande à OpenAI ---
if st.button('Générer la Fiche de Poste'):
    if user_prompt:
        try:
            # Appeler l'API OpenAI avec le prompt de l'utilisateur
            response = openai.Completion.create(
                model="gpt-3.5-turbo",  # Ou gpt-4 si tu l'as
                prompt=user_prompt,
                max_tokens=500
            )
            
            # Afficher la réponse générée par ChatGPT
            st.subheader('Fiche de Poste Générée:')
            st.write(response.choices[0].text.strip())
        
        except Exception as e:
            st.error(f"Erreur lors de la génération de la fiche de poste : {e}")
    else:
        st.warning("Veuillez entrer un prompt avant de soumettre.")

# --- Ajouter un bouton pour générer les fiches de poste depuis le fichier RPO ---
if st.button('Générer à partir du fichier RPO'):
    # Récupérer et traiter les données du fichier RPO
    try:
        donnees_rpo = recuperer_donnees_google_sheet()

        for poste_selectionne in donnees_rpo:
            # Vérifier si les données sont présentes avant de les ajouter
            titre_poste = poste_selectionne.get('Titre du poste recherché', None)
            duree_mission = poste_selectionne.get('Durée de la mission', '6 mois')  # Si vide, mettre 6 mois
            statut_mission = poste_selectionne.get('statut mission', None)
            salaire = poste_selectionne.get('Salaire', None)
            teletravail = poste_selectionne.get('Télétravail', None)
            date_demarrage = poste_selectionne.get('Date de démarrage', None)
            competences = poste_selectionne.get('Compétences obligatoires', None)
            projet = poste_selectionne.get('Projet sur lequel va travailler le ou la candidate :', None)
            client = poste_selectionne.get('Nom du client', None)
            localisation = poste_selectionne.get('Localisation', None)

            # Construire le prompt en n'ajoutant que les informations disponibles
            prompt_fiche = "Description du poste :\n"

            if titre_poste:
                prompt_fiche += f"- Titre du poste recherché : {titre_poste}\n"
            if duree_mission:
                prompt_fiche += f"- Durée de la mission : {duree_mission}\n"
            if statut_mission:
                prompt_fiche += f"- Statut mission : {statut_mission}\n"
            if projet:
                prompt_fiche += f"- Projet : {projet}\n"
            if competences:
                prompt_fiche += f"- Compétences : {competences}\n"
            if salaire:
                prompt_fiche += f"- Salaire : {salaire}\n"
            if teletravail:
                prompt_fiche += f"- Télétravail : {teletravail}\n"
            if date_demarrage:
                prompt_fiche += f"- Date de démarrage : {date_demarrage}\n"
            if localisation:
                prompt_fiche += f"- Localisation : {localisation}\n"

            # Appeler l'API OpenAI pour générer la fiche de poste
            response = openai.Completion.create(
                model="gpt-3.5-turbo",  # Ou gpt-4 si tu l'as
                prompt=prompt_fiche,
                max_tokens=500
            )

            # Afficher la réponse générée par ChatGPT
            st.subheader(f'Fiche de Poste pour {titre_poste}:')
            st.write(response.choices[0].text.strip())
        
    except Exception as e:
        st.error(f"Erreur lors de la récupération ou du traitement des données : {e}")
