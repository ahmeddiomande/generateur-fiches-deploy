import streamlit as st
import os
from pathlib import Path
import zipfile

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Générateur de Fiches de Poste", page_icon="📝", layout="wide")

# --- LOGO ET TITRE ---
st.image("Sans titre.png", width=200)
st.markdown("<h1 style='color:#4e5a78;'>JOB CREATOR - IDEALMATCH</h1>", unsafe_allow_html=True)

# --- MENU DE NAVIGATION ---
st.sidebar.title("📁 Menu Principal")
menu = st.sidebar.radio("Choisissez une section :", [
    "📄 Création via un fichier CSV",
    "🧾 Création via un formulaire IDEALMATCH",
    "📤 Export des fiches de poste (JOB.py)",
    "📥 Génération RPO (DESK.py)",
    "🔍 Étude des candidats (🔒 en développement)"
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

    fichier_xlsx = Path("data/fichier_cible.xlsx")
    if fichier_xlsx.exists():
        with open(fichier_xlsx, "rb") as f:
            st.download_button(
                label="📥 Télécharger le fichier Excel avec liens",
                data=f,
                file_name="Fiches_IDEALMATCH.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("⚠️ Aucun fichier Excel généré trouvé.")

# --- SECTION 4 : DESK.py ---
elif menu == "📥 Génération RPO (DESK.py)":
    st.subheader("Récupération des données Google Sheets (DESK.py)")

    if st.button("Lancer le script DESK.py"):
        os.system("python DESK.py")
        st.success("✅ RPO généré et prêt à être téléchargé.")

    rpo_path = Path("data/fichier_cible.xlsx")
    fiches_path = Path("fiches/")
    mails_path = Path("mails/")

    # Créer le fichier ZIP contenant le RPO, les fiches et les mails
    if rpo_path.exists() and fiches_path.exists() and mails_path.exists():
        # Créer un fichier ZIP
        zip_file = "output/pack_fiches_rpo.zip"
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Ajouter le fichier RPO
            zipf.write(rpo_path, "fichier_cible.xlsx")

            # Ajouter les fiches de poste
            for fiche in fiches_path.glob("*.docx"):
                zipf.write(fiche, fiche.name)

            # Ajouter les mails
            for mail in mails_path.glob("*.docx"):
                zipf.write(mail, mail.name)

        # Télécharger le fichier ZIP
        with open(zip_file, "rb") as f:
            bytes_data = f.read()
        st.download_button(
            label="📥 Télécharger le fichier ZIP",
            data=bytes_data,
            file_name="pack_fiches_rpo.zip",
            mime="application/zip"
        )
    else:
        st.info("⚠️ Aucun fichier RPO, fiches de poste ou mails détectés pour le moment.")

# --- SECTION 5 : Étude des candidats ---
elif menu == "🔍 Étude des candidats (🔒 en développement)":
    st.subheader("🔒 Fonctionnalité bientôt disponible !")
    st.info("Cette section sera bientôt activée pour l'analyse intelligente des candidats.")
