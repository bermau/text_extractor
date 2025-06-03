# Le but est d'étudier le log de la connexion DMS

import os
import sys
import re
from datetime import datetime, timedelta
from collections import deque, defaultdict
import matplotlib.pyplot as plt
import glob

REP = "../data_in/dms"

FILES = [
"DMS_dem_20250524_114214.log",
"DMS_dem_20250525_114225.log",
"DMS_dem_20250526_114237.log",
"DMS_dem_20250526_173047.log",
"DMS_dem_20250526_174551.log",
"DMS_dem_20250527_174648.log"
]


class LogViewer():
    def __init__(self, files_lst, date_pattern=None, bloc_min=60, context_lines=2, keywords=None,
                 start_time = None, stop_time = None):
        """

        :param files_lst:
        :param date_pattern:
        :param bloc_min:             # duration of each period in minutes.
        :param context_lines:        # Nombre de lignes de contexte avant et après

        """
        self.files = files_lst
        self.date_pattern = date_pattern
        self.block_min = bloc_min
        self.context_lines = context_lines

        # Mots-clés à détecter
        self.keywords= keywords
        if self.keywords is None:
            self.keywords= ["WARNING", "ERROR"]

        # Dictionnaire pour compter les erreurs par tranche de N minute
        self.time_counts = {keyw: defaultdict(int) for keyw in self.keywords}

        self.first_time = None     # first_time représente la première demi-heure où une erreur est détectée, pas le début du fichier log.
        self.last_time = None
        if self.date_pattern is None:
            self.date_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"

        self.start_time = start_time or datetime(2025, 5, 20, 1)  # datetime compris
        self.stop_time = stop_time or datetime(2025, 6, 30, 10)  # datetime non compris


    def examine_logs(self):
        # définit le fait d'être dans la période d'étude (entre les 2 date start_time et stop_time)
        study_state = 0  # 0 : avant, 1 : pendant, 2 après

        # Chemin vers le fichier log
        for file in self.files:
            log_file = file
            # os.path.join(REP, file)

            with open(log_file, "r", encoding="ANSI") as f:
                buffer = deque(maxlen=self.context_lines)
                show_post = 0

                for line in f:
                    date_match = re.search(self.date_pattern, line, re.IGNORECASE)
                    if date_match:
                        log_date = datetime.strptime(date_match.group(), "%Y-%m-%d %H:%M:%S")

                        # Déterminer si on est dans la période d'étude.
                        if study_state == 0:
                            if log_date >= self.start_time:
                                study_state = 1
                        elif study_state == 1:
                            if log_date >= self.stop_time:
                                study_state = 2

                        if study_state == 1:
                            # Regrouper les erreurs par NN minute. Arrondir à la période inférieure
                            minute_block = (log_date.minute // self.block_min) * self.block_min
                            log_half_hour = log_date.replace(minute=minute_block, second=0)

                            # repérer le début et la fin des erreurs
                            if not self.first_time or log_half_hour < self.first_time:
                                self.first_time = log_half_hour
                            if not self.last_time or log_half_hour > self.last_time:
                                self.last_time = log_half_hour

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
                        for keyword in self.keywords:
                            if keyword in line and date_match:
                                self.time_counts[keyword][log_half_hour] += 1

                                # Afficher le buffer (qui contient la ligne actuelle et la précédente)
                                print("------")
                                for ctx_line in buffer:
                                    print(ctx_line.strip())
                                show_post = self.context_lines

    def make_graph(self):
        # Générer un graphique
        if any(self.time_counts[k] for k in self.keywords):

            full_range = []
            current = self.first_time

            while current <= self.last_time:
                full_range.append(current)

                for kw in self.keywords:
                    if current not in self.time_counts[kw]:
                        self.time_counts[kw][current] = 0
                current += timedelta(minutes=self.block_min)

            full_range.sort()

            plt.figure(figsize=(12, 5))
            for kw in self.keywords:
                counts = [self.time_counts[kw][t] for t in full_range]
                plt.plot(full_range, counts, marker='o', label=kw)

            plt.title(f"Nombre d'erreurs par {self.block_min} minutes (Fichiers : {motif})")
            plt.xlabel("Temps")
            plt.ylabel("Nombre d'erreurs")
            plt.grid(True)
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            print("Aucune erreur détectée pour générer un graphique.")


if __name__ == '__main__':
    # On va extraire tous les fichiers ayant un même motif.
    motif = "xn"
    files_batch = "../data_in/dms_2/" + motif + "*.log"
    FILES = glob.glob(files_batch)

    C = LogViewer(FILES, bloc_min=120)
    C.examine_logs()
    C.make_graph()

