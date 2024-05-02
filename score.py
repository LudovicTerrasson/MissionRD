import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score
from sklearn.metrics import confusion_matrix
import seaborn
import matplotlib.pyplot as plt

#Fonction pour calculer la précision globale du chatbot
def accuracy(list_predictions, list_data_test):
    nb_folds = len(list_predictions)
    somme = 0
    L=[]
    for i in range(nb_folds):
        len_expected = len(list_data_test[i])
        expected = list_data_test[i]
        val = sum([expected[j]==list_predictions[i][j] for j in range(len_expected)])/len_expected
        L.append(val)
        somme += val
    somme = somme/nb_folds
    return somme

#Fonction pour calculer la précision par niveau de difficulté
def accuracy_by_difficulty(list_predictions, list_data_test, list_difficulty):
    difficulty_levels = [0, 1, 1.5, 2, 2.5]
    accuracy_by_difficulty = {level: [] for level in difficulty_levels}
    nb_folds = len(list_predictions)
    for i in range(nb_folds):
        len_expected = len(list_data_test[i])
        expected = list_data_test[i]
        difficulty = list_difficulty[i]
        val = sum([expected[j]==list_predictions[i][j] for j in range(len_expected)])/len_expected
        accuracy_by_difficulty[difficulty].append(val)
    avg_accuracy_by_difficulty = {level: np.mean(accuracy_by_difficulty[level]) for level in difficulty_levels}
    return avg_accuracy_by_difficulty

#Fonction pour calculer la précision par motif
def accuracy_by_motif(list_predictions, list_data_test, list_motif):
    unique_motifs = set(list_motif)
    accuracy_by_motif = {motif.strip(): {'accuracy': [], 'occurrences': 0} for motif in unique_motifs}
    nb_folds = len(list_predictions)
    for i in range(nb_folds):
        len_expected = len(list_data_test[i])
        expected = list_data_test[i]
        motif = list_motif[i].strip()
        val = sum([expected[j] == list_predictions[i][j] for j in range(len_expected)]) / len_expected
        accuracy_by_motif[motif]['accuracy'].append(val)
        accuracy_by_motif[motif]['occurrences'] += len_expected
    avg_accuracy_by_motif = {
        motif: {
            'accuracy': np.mean(accuracy_by_motif[motif]['accuracy']),
            'occurrences': accuracy_by_motif[motif]['occurrences']
        }
        for motif in accuracy_by_motif
    }
    return avg_accuracy_by_motif

#Fonction pour afficher la précision par niveau de difficulté
def display_accuracy_by_difficulty(score_accuracy_by_difficulty):
    for level, accuracy in score_accuracy_by_difficulty.items():
        print(f"Précision par niveau de difficulté {level}: {accuracy}")
    print("\n")

#Fonction pour afficher la précision par motif
def display_accuracy_by_motif(sorted_accuracy_by_motif):
    for motif, data in sorted_accuracy_by_motif.items():
        accuracy = data['accuracy']
        occurrences = data['occurrences']
        print(f"Précision motif '{motif}': {accuracy}, {occurrences} apparitions")

# Chargement des données
chemin_fichier_excel = "C:/Users/lucie/Documents/EMA/2A/2IA/Mission R&D/RD_2024/data_correctes/Mairie_Roanne.xlsx"
df = pd.read_excel(chemin_fichier_excel)

# Colonnes à utiliser
colonnes_predictions = ['motif_llama_Neural']
colonnes_valeurs_attendues = ['motif']

# Prétraitement des données
predictions = df[colonnes_predictions].astype(str).apply(lambda x: x.str.strip().str.lower()).values.tolist()
valeurs_attendues = df[colonnes_valeurs_attendues].astype(str).apply(lambda x: x.str.strip().str.lower()).values.tolist()

# Calcul de la précision globale
score_accuracy = accuracy(predictions, valeurs_attendues)
print("Précision globale:", score_accuracy)
print("\n")

# Calcul de la précision par niveau de difficulté
df['difficulté'] = df['difficulté'].str.replace(',', '.').astype(float)
score_accuracy_by_difficulty = accuracy_by_difficulty(predictions, valeurs_attendues, df['difficulté'])
display_accuracy_by_difficulty(score_accuracy_by_difficulty)

# Calcul de la précision par motif
score_accuracy_by_motif = accuracy_by_motif(predictions, valeurs_attendues, df['motif'])
sorted_accuracy_by_motif = dict(sorted(score_accuracy_by_motif.items(), key=lambda item: item[1]['accuracy'], reverse=True))
display_accuracy_by_motif(sorted_accuracy_by_motif)
