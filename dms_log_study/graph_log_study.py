# Le but est d'étudier le log de la connexion DMS

import os
import sys
import re
from datetime import datetime, timedelta
from collections import deque, defaultdict
import matplotlib.pyplot as plt

import glob
import local_param
import subprocess
from pathlib import Path

INPUT_REP = "../data_in/dms_2"

FILES = [
    "DMS_dem_20250524_114214.log",
    "DMS_dem_20250525_114225.log",
    "DMS_dem_20250526_114237.log",
    "DMS_dem_20250526_173047.log",
    "DMS_dem_20250526_174551.log",
    "DMS_dem_20250527_174648.log"
]


class Fetcher:
    """Outils pour récupérer des fichiers"""

    def __init__(self, repertory):
        self.repertory = repertory
        self.login = None
        self.pw = None

    def define_session(self):
        "Demande user/mp"
        self.host = local_param.host
        self.login = local_param.lg
        self.pw = local_param.pw

    def recuperer_logs_scp(self, host, username, password, repertoire_distant, repertoire_local):
        """
        Récupère les fichiers de logs via scp
        """

        # Créer le répertoire local s'il n'existe pas
        Path(repertoire_local).mkdir(parents=True, exist_ok=True)

        # Utiliser le fichier de config SSH de l'utilisateur
        ssh_config = os.path.expanduser("~/AppData/Roaming/MobaXterm/home/.ssh/config")

        print(f"Utiliser {ssh_config=}")

        known_hosts_path = r"C:\Users\U178211\AppData\Roaming\MobaXterm\home\.ssh\known_hosts"
        # Commande scp pour récupérer tous les fichiers du répertoire REP
        commande = [
            "scp",
            "-o", f"UserKnownHostsFile={known_hosts_path}",
            "-o", "HostKeyAlgorithms=+ssh-rsa,ssh-dss",
            "-o", "PubkeyAcceptedKeyTypes=+ssh-rsa,ssh-dss",
            "-F", ssh_config,  # utiliser la config SSH
            "-r",  # récursif
            f"{username}@{host}:{repertoire_distant}/*",
            repertoire_local
        ]

        try:
            # Utiliser Popen pour pouvoir envoyer le mot de passe
            process = subprocess.Popen(
                commande,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Envoyer le mot de passe si demandé
            stdout, stderr = process.communicate(input=f"{password}\n")

            if process.returncode == 0:
                print("Téléchargement réussi !")
                return True
            else:
                print(f"Erreur scp : {stderr}")
                return False

        except Exception as e:
            print(f"Erreur lors de l'exécution : {e}")
            return False


class BlockManipulator:
    """Manip sur un bloc de N lignes"""

    def __init__(self, nb):
        self.nb = nb
        self.buffer = deque(maxlen=nb)
        for _ in range(nb):
            self.buffer.append("None")
        self.date_match = False

    def append(self, qqchose):
        self.buffer.append(qqchose)

    def if_date_and_context_match(self, date_pattern, txt_pattern):
        """
        Test si la ligne du milieu contient une date est les lignes du centre contiennent des mots clés
        :param date_pattern:
        :param txt_pattern:  list of pattern mathc for pre-line, lien and post-line
        :return:
        """
        self.date_match = re.search(date_pattern, self.buffer[2], re.IGNORECASE)
        pre_condition = txt_pattern[0] in self.buffer[1]
        post_condition = txt_pattern[2] in self.buffer[3]
        return self.date_match and pre_condition and post_condition

    @property
    def main_line(self):
        return self.buffer[2]

    def afficher(self):
        print("-----------")
        for line in self.buffer:
            print(line.strip())


class LogViewer:
    def __init__(self, files_lst, date_pattern=None, bloc_min=60, context_lines_nb=2, motif=None, keywords=None,
                 contextual_kwds=None,
                 start_time=None, stop_time=None):
        """
        :param files_lst:
        :param date_pattern:
        :param bloc_min:             # duration of each period in minutes.
        :param context_lines_nb:        # Nombre de lignes de contexte avant et après

        """
        self.files = files_lst
        self.date_pattern = date_pattern
        self.block_min = bloc_min
        self.context_lines_nb = context_lines_nb

        # Mots-clés à détecter
        self.motif= motif
        self.keywords = keywords or ["ERROR", "WARNING"]

        # Dictionnaire pour compter les erreurs par tranche de N minute
        self.time_counts = {keyw: defaultdict(int) for keyw in self.keywords}

        self.first_time = None  # first_time représente la première demi-heure où une erreur est détectée, pas le début du fichier log.
        self.last_time = None

        self.date_pattern = date_pattern or r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
        # detect_word
        context_word = "Unreadable"
        self.contextual_kwds = contextual_kwds or ["", "", context_word]

        self.start_time = start_time or datetime(2025, 5, 20, 1)  # datetime compris
        self.stop_time = stop_time or datetime(2025, 6, 30, 10)  # datetime non compris

    def examine_logs(self):
        # définit le fait d'être dans la période d'étude (entre les 2 date start_time et stop_time)
        study_state = 0  # 0 : avant, 1 : pendant, 2 après

        # Chemin vers le fichier log
        for file in self.files:
            log_file = file

            with open(log_file, "r", encoding="ANSI") as f:
                # buffer = deque(maxlen=self.context_lines_nb)
                buffer_5 = BlockManipulator(5)
                show_post = 0

                for line in f:
                    if line == "\n":
                        continue
                    # print(f"Line : {line.strip()}")
                    # date_match = buffer.if_date_and_context_match(self.date_pattern)

                    # Retenir la ligne dans un buffer de 2 lignes (paramétrable).
                    buffer_5.append(line)

                    criteria_match = buffer_5.if_date_and_context_match(self.date_pattern, self.contextual_kwds)

                    if criteria_match:
                        log_date = datetime.strptime(buffer_5.date_match.group(), "%Y-%m-%d %H:%M:%S")

                        # Déterminer si on est dans la période d'étude.
                        if study_state == 0:  # avant
                            if log_date >= self.start_time:
                                study_state = 1
                        elif study_state == 1:  # pendant
                            if log_date >= self.stop_time:
                                study_state = 2  # après

                        if study_state == 1:
                            # Regrouper les erreurs par NN minute. Arrondir à la période inférieure
                            minute_block = (log_date.minute // self.block_min) * self.block_min
                            period_of_log = log_date.replace(minute=minute_block, second=0)

                            # repérer le début et la fin des erreurs
                            if not self.first_time or period_of_log < self.first_time:
                                self.first_time = period_of_log
                            if not self.last_time or period_of_log > self.last_time:
                                self.last_time = period_of_log

                    # tout le reste n'est effectué qu'en cours d'étude
                    if (study_state == 1) and criteria_match:
                        # Afficher le contexte qui suit un mot clé précédemment détecté

                        # # Ajout d'un filtre : il faut un mot-clé dans la ligne pré contexte
                        # # Rechercher les mots clés et mettre à jour le dictionnaire compteur de mots.
                        for keyword in self.keywords:
                            if keyword in buffer_5.main_line and criteria_match:
                                self.time_counts[keyword][period_of_log] += 1
                                buffer_5.afficher()


    def make_graph(self, title=None, annotations=None):

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

            # plt.figure(figsize=(12, 5))
            fig, ax1 = plt.subplots(figsize=(12, 5))

            for kw in self.keywords:
                counts = [self.time_counts[kw][t] for t in full_range]
                plt.plot(full_range, counts, marker='o', label=kw)

            # Afficher les annotations
            if annotations:
                for i, (la_date, label) in enumerate(annotations, start=1):
                    if (la_date >= full_range[0]) and (la_date <= full_range[-1]):
                         ax1.annotate(label, xy=(la_date, 10*i)
                                      , rotation=0
                                      , ha= 'left'
                                      , va = 'bottom'
                                      # , arrowprops=dict(facecolor='black',  arrowstyle="simple", connectionstyle="arc3,rad=-0.2")
                                      , arrowprops=dict(facecolor='black', arrowstyle="->"
                                                        # connectionstyle="angle3,angleA=0,angleB=90"
                                                        ,shrinkA=0, shrinkB=0
                                                        )
                         )

            # Afficher les titres
            if title:
                whole_title = title + "\n"
            else:
                whole_title = ""
            whole_title += f"""
Nombre d'erreurs par {self.block_min} minutes (Fichiers : {self.motif} {self.keywords}, )
contexte : {self.contextual_kwds}
"""

            plt.title(whole_title)
            plt.xlabel("Temps")
            plt.ylabel("Nombre d'erreurs")
            plt.grid(True)
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()

            plt.show(block=True)
        else:
            print("Aucune erreur détectée pour générer un graphique.")


def demo_repartation_code_barre():
    # Etude du dysfonctionnement du moteur du lecteur de codes-barres.

    motif = "glimsonl20"
    kw = ["WARNING"]

    annotations = [(datetime(2025, 6, 4, 18), "Orientation privilégiée des tubes")
        , (datetime(2025, 6, 5, 14), "Intervention sur lecteur de code-barres")
                   ]

    files_batch = "../data_in/dms_2/" + motif + "*.log"
    FILES = glob.glob(files_batch)

    C = LogViewer(FILES, bloc_min=60, keywords=kw, motif = motif, contextual_kwds=["", "", "Unreadable"])
    C.examine_logs()
    C.make_graph(title="Recherche des erreurs de codes-barres", annotations=annotations)

def demo_recherche_arret_DMS():
    # # On va extraire tous les fichiers ayant un même motif.
    # global motif

    motif = "DMS_dem"
    kw =["ERROR"]

    annotations = None

    files_batch = "../data_in/dms_2/" + motif + "*.log"
    FILES = glob.glob(files_batch)

    C = LogViewer(FILES
                  , bloc_min=60
                  , keywords=kw
                  , start_time=datetime(2025, 6, 10, 0)
                  # , stop_time=datetime(2025, 6, 6, 0)
                  , motif = motif
                  , contextual_kwds=["", "", ""]
                  )

    C.examine_logs()
    C.make_graph(title="Recherche arrêt DMS", annotations=annotations)


def demo_cyberlab_PROD():
    """Etude pour Cyberlab  et glimsonl2"""

    motif = "glimsonl2"
    motif = "houl"
    kw =["ERROR"]

    annotations = None

    files_batch = "../data_in/dms_2/" + motif + "*.log"
    FILES = glob.glob(files_batch)

    C = LogViewer(FILES
                  , bloc_min=60
                  , keywords=kw
                  , start_time=datetime(2025, 6, 12, 0)
                  # , stop_time=datetime(2025, 6, 6, 0)
                  , motif = motif
                  , contextual_kwds=["", "", ""]
                  )

    C.examine_logs()
    C.make_graph(title="Recherche sur Cyberlab PROD", annotations=annotations)
def demo_temoin_valab():

    motif = "valab"
    kw =["ERROR"]
    annotations = None
    files_batch = "../data_in/dms_2/" + motif + "*.log"
    FILES = glob.glob(files_batch)

    C = LogViewer(FILES
                  , bloc_min=60
                  , keywords=kw
                  , start_time=datetime(2025, 5, 9, 0)
                  # , stop_time=datetime(2025, 6, 6, 0)
                  , motif = motif
                  , contextual_kwds=["", "", ""]
                  )

    C.examine_logs()
    C.make_graph(title="Témoin connexion valab", annotations=annotations)

def demo_recup_logs():
    trl_rep = "../data_in/dms_2/"
    fetcher = Fetcher(os.path.join(trl_rep,'valab'))
    fetcher.define_session()

    rep_distant= os.path.join(trl_rep, "valab")
    print(f"{rep_distant=}")

    fetcher.recuperer_logs_scp(fetcher.host, fetcher.login,
                               fetcher.pw,
                               repertoire_distant= os.path.join(trl_rep, "valab"),
                               repertoire_local=INPUT_REP)

if __name__ == '__main__':

    # demo_temoin_valab()
    demo_cyberlab_PROD()

