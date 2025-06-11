import paramiko
from scp import SCPClient
import getpass
import local_param

# === CONFIGURATION ===
hostname = local_param.host
port = 22
username = local_param.lg
log_path = "/mips/glims8/log/trl/scan_twain/scan_twain_20201109_121524.log"
local_path = "./machin.log"

# === DEMANDE DU MOT DE PASSE ===
input("Début...")
password = getpass.getpass("Mot de passe SSH : ")

# === CONNEXION SSH ===
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, port=port, username=username, password=password)

# === COPIE DU FICHIER ROOT VERS TON HOME ===
tmp_path = f"/home/{username}/labo/temp_log.log"
print(f"[+] Copie du fichier root avec sudo vers {tmp_path}...")
stdin, stdout, stderr = client.exec_command(f"sudo cp {log_path} {tmp_path} && sudo chown {username}:{username} {tmp_path}")
stdout.channel.recv_exit_status()  # attend la fin

# === TÉLÉCHARGEMENT VIA SCP ===
print(f"[+] Téléchargement via SCP vers {local_path}...")
with SCPClient(client.get_transport()) as scp:
    scp.get(tmp_path, local_path)

# === SUPPRESSION TEMPORAIRE (facultatif) ===
print("[+] Suppression du fichier temporaire...")
client.exec_command(f"rm {tmp_path}")

# === FERMETURE ===
client.close()
print("[✓] Fichier récupéré avec succès.")
