import spacy
import random
import speech_recognition as sr
from gtts import gTTS
import os
import pyttsx3


# Charger le modèle spaCy pour le français
nlp = spacy.load("fr_core_news_sm")

# Liste de réponses possibles
reponses = {
    "bonjour": ["Bonjour! Comment puis-je vous aider aujourd'hui?", "Salut! En quoi puis-je vous assister?", "Hello! Quelle est votre demande?"],
    "horaires": ["Les horaires d'ouverture de la mairie sont du lundi au vendredi de 9h à 17h.", "La mairie est ouverte en semaine de 9h à 17h."],
    "services": ["La mairie propose divers services tels que l'inscription à des événements, la délivrance de documents, etc.", "Nos services incluent l'assistance administrative, l'information sur les événements locaux, etc."],
    "au revoir": ["Au revoir! N'hésitez pas à revenir si vous avez d'autres questions.", "À bientôt! Si vous avez besoin d'aide, je suis là."],
    "carte d'identité": ["Pour demander une carte d'identité, veuillez suivre ces étapes:\n1. Présentez-vous en personne à la mairie.\n2. Apportez les documents requis (photo d'identité, justificatif de domicile, etc.).\n3. Remplissez le formulaire de demande sur place.\n4. Payez les frais de traitement, le cas échéant.\n5. Attendez la notification pour récupérer votre carte d'identité."],
    "permis de construire": ["Pour obtenir un permis de construire, suivez ces étapes:\n1. Consultez le service d'urbanisme de la mairie.\n2. Préparez les documents nécessaires (plans, autorisations, etc.).\n3. Remplissez le formulaire de demande.\n4. Soumettez votre demande et attendez l'approbation."],
    "passeport": ["Pour obtenir un passeport, suivez ces étapes:\n1. Prenez rendez-vous au service des passeports de la mairie.\n2. Apportez les documents requis (photo d'identité, justificatif de domicile, etc.).\n3. Remplissez le formulaire de demande sur place.\n4. Payez les frais de traitement.\n5. Attendez la notification pour récupérer votre passeport."],
    "mariage": ["Pour célébrer un mariage à la mairie, suivez ces étapes:\n1. Prenez rendez-vous au service d'état civil.\n2. Apportez les documents requis (pièces d'identité, justificatif de domicile, etc.).\n3. Choisissez une date de cérémonie disponible.\n4. Participez à la cérémonie de mariage à la mairie."],
    "inscription à l'école": ["Pour inscrire votre enfant à l'école, veuillez suivre ces étapes:\n1. Contactez l'école de votre choix.\n2. Apportez les documents requis (certificat de naissance, carnet de vaccination, etc.).\n3. Remplissez le formulaire d'inscription.\n4. Attendez la confirmation de l'inscription."],
    "prise de rendez-vous": ["Pour prendre un rendez-vous à la mairie, suivez ces étapes:\n1. Appelez le service approprié pour fixer un rendez-vous.\n2. Expliquez le motif du rendez-vous.\n3. Confirmez la date et l'heure du rendez-vous.\n4. Présentez-vous à la mairie à l'heure convenue."],
    "passeport biométrique": ["Pour obtenir un passeport biométrique, suivez ces étapes:\n1. Prenez rendez-vous au service des passeports de la mairie.\n2. Apportez les documents requis (photo d'identité, justificatif de domicile, etc.).\n3. Remplissez le formulaire de demande sur place.\n4. Payez les frais de traitement.\n5. Attendez la notification pour récupérer votre passeport biométrique."],
    "déclaration de naissance": ["Pour faire une déclaration de naissance à la mairie, suivez ces étapes:\n1. Apportez le certificat médical de naissance.\n2. Présentez-vous au service d'état civil.\n3. Remplissez le formulaire de déclaration de naissance.\n4. Obtenez le livret de famille."],
    "certificat de résidence": ["Pour obtenir un certificat de résidence, suivez ces étapes:\n1. Apportez les documents justificatifs (factures, bail, etc.).\n2. Présentez-vous au service d'état civil.\n3. Remplissez le formulaire de demande.\n4. Recevez le certificat de résidence."],
    "renouvellement de carte d'identité": ["Pour renouveler votre carte d'identité, suivez ces étapes:\n1. Présentez-vous en personne au service d'état civil.\n2. Apportez les documents requis (photo d'identité, justificatif de domicile, etc.).\n3. Remplissez le formulaire de renouvellement sur place.\n4. Payez les frais de traitement, le cas échéant.\n5. Attendez la notification pour récupérer votre carte renouvelée."],
    "certificat de mariage": ["Pour obtenir un certificat de mariage, suivez ces étapes:\n1. Présentez-vous au service d'état civil avec les pièces d'identité des époux.\n2. Remplissez le formulaire de demande de certificat de mariage.\n3. Payez les frais de traitement.\n4. Recevez le certificat de mariage."],
    "demande de subvention": ["Pour faire une demande de subvention à la mairie, suivez ces étapes:\n1. Consultez le service des affaires sociales.\n2. Obtenez le formulaire de demande de subvention.\n3. Remplissez le formulaire avec les détails de votre projet.\n4. Soumettez votre demande et attendez l'évaluation."],
    "certificat de décès": ["Pour obtenir un certificat de décès, suivez ces étapes:\n1. Présentez-vous au service d'état civil avec le certificat de décès.\n2. Remplissez le formulaire de demande de certificat de décès.\n3. Payez les frais de traitement, le cas échéant.\n4. Recevez le certificat de décès."],
    "déclaration de changement d'adresse": ["Pour faire une déclaration de changement d'adresse, suivez ces étapes:\n1. Présentez-vous au service d'état civil.\n2. Apportez une pièce d'identité et un justificatif de domicile.\n3. Remplissez le formulaire de déclaration de changement d'adresse.\n4. Recevez la confirmation du changement d'adresse."],
    "demande d'aide sociale": ["Pour faire une demande d'aide sociale, suivez ces étapes:\n1. Consultez le service des affaires sociales.\n2. Expliquez votre situation et obtenez le formulaire de demande d'aide sociale.\n3. Remplissez le formulaire avec les détails nécessaires.\n4. Soumettez votre demande et attendez l'évaluation."],
    "démarches pour le vote": ["Pour effectuer les démarches liées au vote, suivez ces étapes:\n1. Vérifiez votre inscription sur les listes électorales.\n2. Contactez le service des élections pour obtenir des informations sur les prochaines élections.\n3. Effectuez les démarches nécessaires pour voter (inscription, procuration, etc.).\n4. Participez aux élections à la date prévue."],
    "demande de logement social": ["Pour faire une demande de logement social, suivez ces étapes:\n1. Consultez le service du logement social à la mairie.\n2. Obtenez le formulaire de demande de logement social.\n3. Remplissez le formulaire avec les informations requises.\n4. Soumettez votre demande et attendez l'évaluation."],
    "certificat de non-gage": ["Pour obtenir un certificat de non-gage, suivez ces étapes:\n1. Consultez le service des véhicules à la mairie.\n2. Apportez les documents du véhicule (carte grise, etc.).\n3. Remplissez le formulaire de demande de certificat de non-gage.\n4. Recevez le certificat de non-gage."],
    "autorisation de sortie du territoire (AST)": ["Pour obtenir une autorisation de sortie du territoire (AST) pour un mineur, suivez ces étapes:\n1. Consultez le service d'état civil à la mairie.\n2. Apportez les documents requis (pièce d'identité du mineur, autorisation parentale, etc.).\n3. Remplissez le formulaire d'AST.\n4. Recevez l'autorisation de sortie du territoire."],
    "certificat de scolarité": ["Pour obtenir un certificat de scolarité, suivez ces étapes:\n1. Contactez le service de l'éducation à la mairie.\n2. Fournissez les informations nécessaires sur l'élève.\n3. Recevez le certificat de scolarité."],
    "demande d'extrait de casier judiciaire": ["Pour demander un extrait de casier judiciaire, suivez ces étapes:\n1. Consultez le service d'état civil à la mairie.\n2. Apportez une pièce d'identité valide.\n3. Remplissez le formulaire de demande d'extrait de casier judiciaire.\n4. Recevez l'extrait de casier judiciaire."],
    "demande de carte grise": ["Pour demander une carte grise, suivez ces étapes:\n1. Consultez le service des véhicules à la mairie.\n2. Apportez les documents requis (certificat d'immatriculation, justificatif de domicile, etc.).\n3. Remplissez le formulaire de demande de carte grise.\n4. Payez les frais de traitement.\n5. Recevez la carte grise."],
    "inscription sur les listes électorales": ["Pour vous inscrire sur les listes électorales, suivez ces étapes:\n1. Consultez le service des élections à la mairie.\n2. Apportez une pièce d'identité et un justificatif de domicile.\n3. Remplissez le formulaire d'inscription sur les listes électorales.\n4. Recevez la confirmation de votre inscription."],
    "demande de duplicata de carte d'identité": ["Pour obtenir un duplicata de carte d'identité, suivez ces étapes:\n1. Consultez le service d'état civil à la mairie.\n2. Apportez une pièce d'identité et déclarez la perte de votre carte d'identité.\n3. Remplissez le formulaire de demande de duplicata.\n4. Payez les frais de traitement.\n5. Recevez le duplicata de votre carte d'identité."],
    "renouvellement de passeport": ["Pour renouveler votre passeport, suivez ces étapes:\n1. Prenez rendez-vous au service des passeports de la mairie.\n2. Apportez les documents requis (photo d'identité, justificatif de domicile, etc.).\n3. Remplissez le formulaire de renouvellement sur place.\n4. Payez les frais de traitement.\n5. Attendez la notification pour récupérer votre passeport renouvelé."],
    "demande de visa": ["Pour faire une demande de visa, suivez ces étapes:\n1. Consultez le service des affaires étrangères à la mairie.\n2. Obtenez le formulaire de demande de visa.\n3. Remplissez le formulaire avec les détails de votre voyage.\n4. Soumettez votre demande et attendez la réponse."],
}

# Liste de synonymes pour les mots clés
synonymes = {
    "bonjour": ["salut","bonjour", "hello", "coucou"],
    "horaires": ["heures d'ouverture","horaires", "quand ouvert", "quand ferme"],
    "services": ["prestations","services", "offres", "activités"],
    "au revoir": ["bye", "à bientôt","au revoir", "adieu"],
    "carte d'identité": ["carte d'identité","carte d'identité", "CNI", "procédure d'obtention de carte d'identité"],
    "permis de construire": ["permis de construire","permis de construire", "autorisation de construire", "construction"],
    "passeport": ["passeport", "demande de passeport","passeport", "renouvellement de passeport"],
    "mariage": ["mariage", "cérémonie de mariage", "union civile"],
    "inscription à l'école": ["inscription à l'école", "inscrire enfant à l'école", "démarches scolaires"],
    "prise de rendez-vous": ["prendre rendez-vous","prise de rendez-vous", "rendez-vous mairie", "fixer un rendez-vous"],
    "passeport biométrique": ["passeport biométrique", "demande de passeport biométrique","renouvellement passeport biométrique"],
    "déclaration de naissance": ["déclaration de naissance", "nouveau-né", "naissance"],
    "certificat de résidence": ["certificat de résidence", "résidence", "justificatif de domicile"],
    "renouvellement de carte d'identité": ["renouvellement de carte d'identité", "renouveler CNI","nouvelle carte d'identité"],
    "certificat de mariage": ["certificat de mariage", "mariage civil", "acte de mariage"],
    "demande de subvention": ["demande de subvention", "subvention projet", "aide financière"],
    "certificat de décès": ["certificat de décès", "décès", "acte de décès"],
    "déclaration de changement d'adresse": ["déclaration de changement d'adresse", "changer d'adresse","nouvelle adresse"],
    "demande d'aide sociale": ["demande d'aide sociale", "aide sociale", "assistance financière"],
    "démarches pour le vote": ["démarches pour le vote", "inscription sur les listes électorales","participer aux élections"],
    "demande de logement social": ["logement social", "demande de logement", "aide au logement"],
    "certificat de non-gage": ["certificat de non-gage", "véhicule d'occasion","certificat de situation administrative"],
    "autorisation de sortie du territoire (AST)": ["autorisation de sortie du territoire", "AST", "voyage mineur"],
    "certificat de scolarité": ["certificat de scolarité", "attestation scolaire", "document pour l'école"],
    "demande d'extrait de casier judiciaire": ["extrait de casier judiciaire", "casier judiciaire","antécédents judiciaires"],
    "demande de carte grise": ["carte grise", "immatriculation véhicule", "nouvelle plaque d'immatriculation"],
    "inscription sur les listes électorales": ["inscription électorale", "voter", "participer aux élections"],
    "demande de duplicata de carte d'identité": ["duplicata de carte d'identité", "nouvelle carte d'identité","remplacement carte perdue"],
    "renouvellement de passeport": ["renouvellement passeport", "passeport expiré", "nouveau passeport"],
    "demande de visa": ["demande de visa", "voyage à l'étranger", "autorisation de voyage"],
}

def repondre(message):
    # Utiliser la reconnaissance vocale pour obtenir le texte à partir de l'audio
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Dites quelque chose...")
        audio = recognizer.listen(source)

    try:
        # Utiliser l'API Google pour la transcription de la parole
        message = recognizer.recognize_google(audio, language="fr-FR").lower()
        print("Vous: " + message)
    except sr.UnknownValueError:
        print("Désolé, je n'ai pas compris la parole.")
        return "Désolé, je n'ai pas compris la parole. Pouvez-vous reformuler votre question?"
    except sr.RequestError as e:
        print(f"Erreur lors de la requête à l'API Google : {e}")
        return "Erreur lors de la reconnaissance vocale. Veuillez réessayer."

    # Traitement du langage naturel avec spaCy
    doc = nlp(message)

    # Liste des mots-clés trouvés
    mots_cles_trouves = [cle for cle, syn in synonymes.items() if any(token.text in syn for token in doc)]

    for cle, syn in synonymes.items():
        if cle in doc.text:
            return random.choice(reponses[cle])

    # Gérer les cas spécifiques
    if "au revoir" in message:
        return random.choice(reponses["au revoir"])

    # Gérer les cas multiples
    if len(mots_cles_trouves) > 1:
        return traiter_cas_multiples(mots_cles_trouves)

    # Gérer les cas uniques
    if len(mots_cles_trouves) == 1:
        cle_trouvee = mots_cles_trouves[0]
        return random.choice(reponses[cle_trouvee])

    return "Désolé, je ne comprends pas. Pouvez-vous reformuler votre question?"

# Fonction pour la synthèse vocale
def parler(texte):
    # Utiliser gTTS pour convertir le texte en fichier audio
    tts = gTTS(text=texte, lang='fr')
    tts.save("reponse.mp3")

    # Jouer le fichier audio
    os.system("afplay reponse.mp3")  # Pour macOS

# Fonction principale du chatbot
def chatbot_mairie():
    print("Bienvenue! Posez-moi des questions sur la mairie.")

    while True:
        # Obtenir la réponse du chatbot
        response = repondre("")

        # Synthèse vocale de la réponse du chatbot
        parler(response)

        # Afficher la réponse du chatbot
        print("Chatbot:", response)

if __name__ == "__main__":
    chatbot_mairie()
