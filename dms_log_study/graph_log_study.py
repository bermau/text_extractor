# Le but est d'étudier le log de la connexion DMS

import os
import sys
import re
from datetime import datetime, timedelta
from collections import deque, defaultdict
import matplotlib.pyplot as plt
import glob

REP = "../data_in/dms"

files = [
"DMS_dem_20250524_114214.log",
"DMS_dem_20250525_114225.log",
"DMS_dem_20250526_114237.log",
"DMS_dem_20250526_173047.log",
"DMS_dem_20250526_174551.log",
"DMS_dem_20250527_174648.log"
]
# On va extraire tous les fichiers ayant un même motif.
motif = "DMS_dem"
files_batch = "../data_in/dms/" + motif + "*.log"
files = glob.glob(files_batch)


# Nombre de lignes de contexte avant et après
context_lines = 2


# Mots-clés à détecter
keywords = [ "ERROR", "WARNING"]
# Durée des tranches en minutes
block_min = 60

# Pattern pour détecter une date, ici format "2025-05-27 14:55:03"
date_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"

# Dictionnaire pour compter les erreurs par tranche de N minute
time_counts = {keyw: defaultdict(int) for keyw in keywords}
first_time = None  # first_time représente la première demi-heure où une erreur est détectée, pas le début du fichier log.
last_time = None

start_time = datetime(2025, 5, 20, 1 )    # compris
stop_time = datetime(2025, 5, 30, 3)      # non compris
# start_time = datetime(2025, 5, 28, 5 )    # compris
# stop_time = datetime(2025, 5, 29 )      # non compris


# définit le fait d'être dans la période d'étude (entre les 2 date start_time et stop_time)
study_state = 0 # 0 : avant, 1 : pendant, 2 après

# Chemin vers le fichier log

for file in files:
    log_file = file
    # os.path.join(REP, file)

    with open(log_file, "r", encoding="ANSI") as f:
        buffer = deque(maxlen=context_lines)
        show_post = 0


        for line in f:
            date_match = re.search(date_pattern, line, re.IGNORECASE)
            if date_match:
                log_date = datetime.strptime(date_match.group(), "%Y-%m-%d %H:%M:%S")

                # Déterminer si on est dans la période d'étude.
                if study_state == 0:
                    if log_date >= start_time:
                        study_state = 1
                elif study_state == 1:
                    if log_date >= stop_time:
                        study_state = 2

                if study_state == 1:
                    # Regrouper les erreurs par NN minute. Arrondir à la période inférieure
                    minute_block = (log_date.minute // block_min) * block_min
                    log_half_hour = log_date.replace(minute=minute_block, second=0)

                    # repérer le début et la fin des erreurs
                    if not first_time or log_half_hour < first_time:
                        first_time = log_half_hour
                    if not last_time or log_half_hour > last_time:
                        last_time = log_half_hour

            # totu le reste n'a d'intérête qu'n cours d'étude
            if study_state == 1:
                # Afficher le contexte qui suit un mot clé
                if show_post > 0:
                    print(line.strip())
                    show_post -= 1
                    continue

                # Reternir la ligne dans un buffer de 2 lignes (paramétrable).
                buffer.append(line)

                # Rechercher les mots clés et mettre à jour le dictionnaire compteur de mots.
                for keyword in keywords:
                    if keyword in line and date_match:
                        time_counts[keyword][log_half_hour] += 1

                        # Afficher le buffer (qui contient la ligne actuelle et la précédente)
                        print("------")
                        for ctx_line in buffer:
                            print(ctx_line.strip())
                        show_post = context_lines

# Générer un graphique
if any(time_counts[k] for k in keywords):

    full_range = []
    current = first_time

    while current <= last_time:
        full_range.append(current)

        for kw in keywords:
            if current not in time_counts[kw]:
                time_counts[kw][current] = 0
        current += timedelta(minutes=block_min)

    full_range.sort()



    plt.figure(figsize=(12, 5))
    for kw in keywords:
        counts = [time_counts[kw][t] for t in full_range]
        plt.plot(full_range, counts, marker='o', label= kw)

    plt.title(f"Nombre d'erreurs par {block_min} minutes (Fichiers : {motif})")
    plt.xlabel("Temps")
    plt.ylabel("Nombre d'erreurs")
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("Aucune erreur détectée pour générer un graphique.")
