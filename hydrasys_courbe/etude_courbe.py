# Etude des données issues du fichier / in.dat situé dans
# /mips/messages/hhydrasys/phor_good/out.dat
# Je note que toutes les trames commencent par 000300A01
# Je pense avoir compris : chaque intensité est codée par 2 octets en hexadécimal, suivis
# de 2 octets nuls 00.
from matplotlib import pyplot as plt
import numpy as np

with open("data.txt", 'r') as f:
    data = f.readline()

# j'ajoute un caractère '0' en début de chaine.
print(f"{len(data)=}")
data = "00" + data
print(f"{len(data)=}")

def get_groups(dat_str, by = 2, decalage=0 ):
    pairs = [dat_str[i:i+by] for i in range(0, len(dat_str), by)]
    return pairs

valeurs = []
group_by = 2

for i, valeur in enumerate(get_groups(data, by=group_by, decalage=0)):
    if i % group_by != 0 :
        decim = int(valeur, 16)
        valeurs.append(decim)

print(f"{len(valeurs)=}")

x = range(len(valeurs))
y = valeurs

plt.plot(x,y)
plt.show(block=True)