import streamlit as st
import os
import pandas as pd

# --- Configuration de la page ---
st.set_page_config(page_title="Générateur de Fiches de Poste", page_icon="📝", layout="wide")

# --- LOGO ET TITRE ---
st.image("Sans titre.png", width=200)  # Assurez-vous que le logo est dans le bon répertoire
st.markdown("<h1 style='color:#4e5a78;'>JOB CREATOR - IDEALMATCH</h1>", unsafe_allow_html=True)

# --- MENU DE NAVIGATION ---
st.sidebar.title("📁 Menu Principal")
menu = st.sidebar.radio("Choisissez une section :", [
    "📄 Création via un fichier CSV",
    "🧾 Création via un formulaire IDEALMATCH",
    "📤 Export des fiches de poste (JOB.py)",
    "📥 Génération RPO (DESK.py)",
    "🔍 Étude des candidats (🔒 en développement)",
    "🧪 Nouveau Test"  # Nouvel onglet ajouté ici
])

# --- SECTION 1 : CSV ---
if menu == "📄 Création via un fichier CSV":
    st.subheader("Création de fiches de poste à partir d'un fichier CSV")
    uploaded_file = st.file_uploader("Upload du fichier CSV/Excel", type=["csv", "xlsx"])
    if uploaded_file:
        with open("input_temp.csv", "wb") as f:
            f.write(uploaded_file.read())
        st.success("Fichier reçu. Lancement du traitement... (à compléter avec JOB.py)")

# --- SECTION 2 : Formulaire IDEALMATCH ---
elif menu == "🧾 Création via un formulaire IDEALMATCH":
    st.subheader("Création d'une fiche via formulaire IDEALMATCH")
    poste = st.text_input("Intitulé du poste")
    mission = st.text_area("Mission principale")
    competences = st.text_area("Compétences requises (séparées par des virgules)")
    if st.button("Générer la fiche de poste"):
        st.success("Fiche de poste générée (fonctionnalité à connecter)")

# --- SECTION 3 : JOB.py ---
elif menu == "📤 Export des fiches de poste (JOB.py)":
    st.subheader("Lancement de la génération complète via JOB.py")
    if st.button("Exécuter le script JOB.py"):
        os.system("python JOB.py")
        st.success("Script exécuté. Fiches générées.")

# --- SECTION 4 : Génération RPO ---
elif menu == "📥 Génération RPO (DESK.py)":
    st.subheader("Récupération des données Google Sheets (DESK.py)")

    if st.button("Lancer le script DESK.py"):
        os.system("python DESK.py")
        st.success("✅ RPO généré et prêt à être affiché.")

    # Vérification et affichage du fichier RPO dans Streamlit
    EXCEL_FILE_PATH = "output/RPO.xlsx"

    if os.path.exists(EXCEL_FILE_PATH):
        st.write("Affichage des données du fichier RPO :")
        df = pd.read_excel(EXCEL_FILE_PATH)
        st.dataframe(df)  # Affiche les données du fichier Excel dans Streamlit
    else:
        st.info("⚠️ Aucun fichier RPO généré pour le moment.")
        st.write("Assurez-vous que le répertoire 'output/' contient bien le fichier 'RPO.xlsx'.")

# --- SECTION 5 : Étude des candidats ---
elif menu == "🔍 Étude des candidats (🔒 en développement)":
    st.subheader("🔒 Fonctionnalité bientôt disponible !")
    st.info("Cette section sera bientôt activée pour l'analyse intelligente des candidats.")

# --- SECTION 6 : Nouveau Test ---
elif menu == "🧪 Nouveau Test":  # Nouveau onglet ajouté
    st.subheader("Bienvenue dans l'onglet Nouveau Test")
    
    # Bouton dans l'onglet Nouveau Test
    if st.button("Lancer le Nouveau Test"):
        st.write("Le test a été lancé avec succès ! 🎉")
