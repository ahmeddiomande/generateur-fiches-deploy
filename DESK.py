import os
import openpyxl
from docx import Document
import zipfile
from dotenv import load_dotenv

# Charger la clé API OpenAI
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Créer le répertoire `output/` s'il n'existe pas
output_directory = "output"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    print(f"Répertoire {output_directory} créé.")

# --- Création du fichier RPO ---
EXCEL_FILE_PATH = 'data/fichier_cible.xlsx'

# Créer un fichier Excel et le remplir avec les données récupérées (depuis Google Sheets par exemple)
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Feuil1"
# Ajouter les données dans le fichier Excel (là où tu récupères tes données)
wb.save(EXCEL_FILE_PATH)

# --- Création du fichier ZIP ---
zip_file = os.path.join(output_directory, "pack_fiches_rpo.zip")  # Crée le chemin complet du ZIP
with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Ajouter le fichier RPO au ZIP
    zipf.write(EXCEL_FILE_PATH, os.path.basename(EXCEL_FILE_PATH))

    # Générer et ajouter les fiches de poste et les mails
    for row in sheet_rpo.iter_rows(min_row=2, values_only=True):
        if len(row) < 6:
            continue

        # Créer les données pour chaque fiche de poste et mail type
        # Génére les fichiers .docx pour chaque fiche de poste et mail

        # Ajouter la fiche de poste au ZIP
        fiche_poste = generer_fiche_poste(data)
        chemin_fichier_word = f"fiches/{nom_fichier_base}.docx"
        zipf.write(chemin_fichier_word, os.path.basename(chemin_fichier_word))

        # Ajouter le mail type au ZIP
        mail_type = generer_mail_type(data)
        chemin_mail_word = f"mails/{nom_fichier_base}_MAIL.docx"
        zipf.write(chemin_mail_word, os.path.basename(chemin_mail_word))

    print(f"Le fichier ZIP a été créé : {zip_file}")
