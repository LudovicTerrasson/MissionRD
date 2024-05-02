import openpyxl
import re

# Fonction pour lire le fichier texte et récupérer les réponses de la borne
def lire_fichier_texte(nom_fichier):
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
            # Utilisation d'une expression régulière pour trouver les réponses de la borne
            reponses = re.findall(r'Borne\s*:\s*(.*)', contenu)
            return [reponse.strip() for reponse in reponses]
    except FileNotFoundError:
        print("Le fichier spécifié est introuvable.")
        return []

# Fonction pour insérer les réponses de la borne dans la colonne Excel
def inserer_reponses_excel(reponses, chemin_fichier_excel):
    try:
        # Chargement du fichier Excel
        wb = openpyxl.load_workbook(chemin_fichier_excel)
        feuille = wb.active

        # Insérer chaque réponse dans la quatrième colonne
        for i, reponse in enumerate(reponses, 2):  # Commencer à partir de la deuxième ligne
            feuille.cell(row=i, column=4, value=reponse)

        # Enregistrement des modifications
        wb.save(chemin_fichier_excel)
        print("Les réponses de la borne ont été insérées avec succès dans la colonne Excel.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Chemin du fichier texte contenant les réponses de la borne
chemin_fichier_texte = "C:/Users/lucie/Documents/EMA/2A/2IA/Mission R&D/Neural.txt"

# Appel de la fonction pour lire le fichier texte et récupérer les réponses de la borne
reponses = lire_fichier_texte(chemin_fichier_texte)

# Chemin du fichier Excel et appel de la fonction pour insérer les réponses de la borne
chemin_fichier_excel = "C:/Users/lucie/Documents/EMA/2A/2IA/Mission R&D/RD_2024/data_correctes/Mairie_Roanne.xlsx"
inserer_reponses_excel(reponses, chemin_fichier_excel)
