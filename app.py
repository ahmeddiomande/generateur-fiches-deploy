import openai
import streamlit as st

# Remplacer par ta clé API OpenAI
API_KEY = 'ton_clé_api_openai'

openai.api_key = API_KEY

# Interface utilisateur Streamlit
st.title('Générateur de Fiche de Poste')

# Demander à l'utilisateur de saisir son prompt
user_prompt = st.text_area("Écrivez ici votre prompt pour générer une fiche de poste :", 
                          "Entrez ici le prompt pour ChatGPT...")

# Bouton pour envoyer la demande à OpenAI
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
