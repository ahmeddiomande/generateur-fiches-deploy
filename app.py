import openai
import streamlit as st
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API OpenAI depuis le fichier .env
API_KEY = os.getenv("OPENAI_API_KEY")

# Vérifier si la clé API a été correctement chargée
if not API_KEY:
    st.error("La clé API OpenAI est manquante. Assurez-vous qu'elle est dans le fichier .env.")
else:
    openai.api_key = API_KEY

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
""")

# --- Zone de saisie du prompt de l'utilisateur ---
user_prompt = st.text_area("Écrivez ici votre prompt pour générer une fiche de poste :", 
                          "Entrez ici le prompt pour ChatGPT...")

# --- Bouton pour générer la fiche de poste à partir du prompt ---
if st.button('Générer la Fiche de Poste'):
    if user_prompt:
        try:
            # Appeler l'API OpenAI avec le prompt de l'utilisateur
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Ou gpt-4 si tu l'as
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500
            )
            
            # Afficher la réponse générée par ChatGPT
            st.subheader('Fiche de Poste Générée:')
            st.write(response['choices'][0]['message']['content'].strip())
        
        except Exception as e:
            st.error(f"Erreur lors de la génération de la fiche de poste : {e}")
    else:
        st.warning("Veuillez entrer un prompt avant de soumettre.")

# --- Bouton pour générer la fiche de poste à partir du fichier RPO ---
if st.button('Générer à partir du fichier RPO'):
    # Cette partie sera implémentée plus tard pour traiter le fichier RPO
    st.info("Le traitement du fichier RPO sera ajouté ici prochainement.")
