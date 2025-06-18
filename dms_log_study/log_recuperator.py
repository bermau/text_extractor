"""Recupterator : récupérer les logs d'un serveur localement
Utilise paramiko"""
import os
import sys

import paramiko
from scp import SCPClient
import getpass
import local_param
# Dans ce programme, le login et l'hôte sont préenregistrées,

# le mot de passe est demandé.

# === CONFIGURATION ===
hostname = local_param.host
port = 22
username = local_param.lg

remote_path = "/mips/glims8/log/trl/scan_twain/scan_twain_20201109_121524.log"
local_path = os.path.join("../data_in/dms_2", os.path.basename(remote_path))


class LogImporter:

    def __init__(self, hostname, port, username ):
        self.password = None
        self.hostname = hostname
        self.port = port
        self.username = username
        self.current_file = None   # Fichier en cours d'importation

        input("Début...")
        self.password = getpass.getpass("Mot de passe SSH : ")

        # === CONNEXION SSH ===
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname, port=port, username=username, password=self.password)
        self.tmp_path = f"/home/{username}/labo/temp_log.log"
    def import_file(self, filename):

        # === COPIE DU FICHIER ROOT VERS TON HOME ===
        print(f"[+] Copie du fichier root avec sudo vers {self.tmp_path}...")
        stdin, stdout, stderr = self.client.exec_command(f"sudo cp {filename} {self.tmp_path} && sudo chown {username}:{username} {self.tmp_path}")
        stdout.channel.recv_exit_status()  # attend la fin

        # === TÉLÉCHARGEMENT VIA SCP ===
        print(f"[+] Téléchargement via SCP vers {local_path}...")
        with SCPClient(self.client.get_transport()) as scp:
            scp.get(self.tmp_path, local_path)

        # === SUPPRESSION TEMPORAIRE (facultatif) ===
        print("[+] Suppression du fichier temporaire...")
        self.client.exec_command(f"rm {self.tmp_path}")

        # === FERMETURE ===
        self.client.close()
        print("[✓] Fichier récupéré avec succès.")

def demo_recup_un_fichier():

    # Exemple importer tout un répertoire
    FILE = "/mips/glims8/log/trl/scan_twain/scan_twain_20201109_121524.log"

    # Import un fichier.
    log_importer = LogImporter(hostname=hostname, port=port, username = username)
    log_importer.import_file(FILE)

if __name__ == '__main__':

    demo_recup_un_fichier()

