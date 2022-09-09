import random

abr_reussite = ["OK", "Critères satisfaits", 'Satisfaisant']

objets = ["pour l'habilitation initiale","pour le maintien des compétences"]

mot_niveau = ["niveau", "pour le niveau", "pour le niv"]

def alea(lst_of_strings):
    return lst_of_strings[random.randint(0, len(lst_of_strings)-1)]

def phrase_commentaire(objet = 1, niveau = 1):

    return " ".join([alea(abr_reussite),
                     objets[objet],
                     alea(mot_niveau),
                    str(niveau),
                     theme
                    ])

def phrase_conclusion(objet = 1, niveau = 1):

    return " ".join(["OK",
                     objets[objet],
                     alea(mot_niveau),
                    str(niveau),
                     theme
                    ])


theme = "Glims Cyberlab"

print(phrase_commentaire(objet= 0, niveau = 1))
print(phrase_commentaire(objet= 1, niveau = 1))