# Simplifie le fichier de type ls -ltR sur les logs de Glims
# Idée : produire un fichier html  de synthèse.

from datetime import datetime
import re

def parse_ls_lr(contenu):
    resultats = {}
    repertoire_courant = None

    for ligne in contenu.splitlines():
        ligne = ligne.strip()

        # Détection d'un répertoire
        if ligne.startswith("./") and ligne.endswith(":"):
            repertoire_courant = ligne[:-1]  # enlever le ":"
            resultats[repertoire_courant] = None
            continue

        # Détection d'un fichier
        if ligne.startswith("-") and repertoire_courant:
            # Exemple de date : "17 mars 18:40"
            match = re.search(r'(\d{1,2}) (\w+) +(\d{1,2}:\d{2})', ligne)
            if match:
                jour, mois, heure = match.groups()

                # convertir mois FR -> numéro
                mois_fr = {
                    "janv": 1, "févr": 2, "mars": 3, "avr": 4,
                    "mai": 5, "juin": 6, "juil": 7, "août": 8,
                    "sept": 9, "oct": 10, "nov": 11, "déc": 12
                }

                mois_num = mois_fr.get(mois[:4].lower())
                if mois_num is None:
                    continue

                date_obj = datetime(
                    year=2026,  # à adapter si besoin
                    month=mois_num,
                    day=int(jour),
                    hour=int(heure.split(":")[0]),
                    minute=int(heure.split(":")[1])
                )

                # garder la plus récente
                if (resultats[repertoire_courant] is None or
                        date_obj > resultats[repertoire_courant]):
                    resultats[repertoire_courant] = date_obj

    return resultats

if __name__ == "__main__":

    with open("logs/svc_logs.txt", 'r') as f:
        lines = f.read()
        print(lines)

        parse = parse_ls_lr(lines)

    print (parse)
