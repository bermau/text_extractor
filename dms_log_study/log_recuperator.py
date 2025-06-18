"""Recupterator : récupérer les logs d'un serveur localement
Utilise paramiko"""
import os
import sys
from pathlib import PurePosixPath

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


class LogImporter:

    def __init__(self, hostname, port, username):
        self.password = None
        self.hostname = hostname
        self.port = port
        self.username = username
        self.current_file = None  # Fichier en cours d'importation

        input("Début...")
        self.password = input("Mot de passe SSH : ")

        # === CONNEXION SSH ===
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname, port=port, username=username, password=self.password)
        self.tmp_path = f"/home/{username}/labo/temp_log.log"

    def import_file(self, filename, local_path):
        # === COPIE DU FICHIER ROOT VERS TON HOME ===
        print(f"[+] Copie du fichier root avec sudo vers {self.tmp_path}...")
        stdin, stdout, stderr = self.client.exec_command(
            f"sudo cp {filename} {self.tmp_path} && sudo chown {username}:{username} {self.tmp_path}")
        stdout.channel.recv_exit_status()  # attend la fin

        # === TÉLÉCHARGEMENT VIA SCP ===
        print(f"[+] Téléchargement via SCP vers {local_path}...")
        with SCPClient(self.client.get_transport()) as scp:
            scp.get(self.tmp_path, local_path)

        # === SUPPRESSION TEMPORAIRE (facultatif) ===
        print("[+] Suppression du fichier temporaire...")
        self.client.exec_command(f"rm {self.tmp_path}")
        print("[✓] Fichier récupéré avec succès.")

    def close_connexion(self):
        # === FERMETURE ===
        self.client.close()
        print("[✓] Cloture de la connexion.")


def demo_recup_un_fichier():
    remote_path = "/mips/glims8/log/trl/scan_twain/scan_twain_20201109_121524.log"
    local_path = os.path.join("../data_in/dms_2", os.path.basename(remote_path))

    # Import un fichier.
    log_importer = LogImporter(hostname=hostname, port=port, username=username)
    log_importer.import_file(remote_path, local_path)
    log_importer.close_connexion()


def import_repertory(log_importer, remote_dir, local_dir):
    """Import tout un répertoire"""

    try:
        stdin, stdout, stderr = log_importer.client.exec_command(f"sudo ls {remote_dir}")
        stdout.channel.recv_exit_status()
        files = stdout.read().decode().split()

        for filename in files:
            if filename.endswith(".log"):
                remote_path = os.path.join(remote_dir, filename)
                local_path = os.path.join(local_dir, os.path.basename(remote_path))
                log_importer.import_file(remote_path, local_path)
    except Exception as e:
        print(f"Erreur après connexion : {e}")

    finally:  # toujours exécuté, erreur ou pas
        log_importer.close_connexion()


def demo_recup_un_repertoire():
    # Importer tout un répertoire :
    remote_dir = "/mips/glims8/log/trl/scan_twain/"
    local_dir = "../data_in/dms_2"
    log_importer = LogImporter(hostname=hostname, port=port, username=username),
    import_repertory(log_importer, remote_dir, local_dir)

def demo_recup_des_repertoires():
    """Get all logs of a list of repertories"""

    lst = ["/mips/glims8/log/trl/valab/", "/mips/glims8/log/trl/scan_twain/"]
    local_dir = "../data_in/dms_2"

    log_importer = LogImporter(hostname=hostname, port=port, username=username)
    for rep in lst:
        import_repertory(log_importer, rep, local_dir)

    log_importer.close_connexion()


def demo_importer_DMS():
    print("NOUVEAU")
    # Il y a une difficulté join fonctionne pour l'OS local...
    trl_rep = r"/mips/glims8/log/trl"
    lst1 = [PurePosixPath(trl_rep) / rep  for rep in [r"DMS_dem", r"DMS_res", r"DMS_tracking"]  ]
    # os.path.join()
    svc_rep= "/mips/glims8/log/svc"
    lst2 = [PurePosixPath(svc_rep) / rep  for rep in ["glimsonl18", "glimsonl19", "glimsonl20"]]

    lst = lst1 + lst2
    print(lst)

    local_dir = "../data_in/dms_2"

    log_importer = LogImporter(hostname=hostname, port=port, username=username)
    for rep in lst:
        print(f"J'importe le repertoire {rep}")
        import_repertory(log_importer, rep, local_dir)

    log_importer.close_connexion()


if __name__ == '__main__':
    remote_dir = "/mips/glims8/log/trl/DMS_dem"
    local_dir = "../data_in/dms_2"
    log_importer = LogImporter(hostname=hostname, port=port, username=username),
    import_repertory(log_importer, remote_dir, local_dir)