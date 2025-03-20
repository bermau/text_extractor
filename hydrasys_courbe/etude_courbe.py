# Etude des données issues du fichier / in.dat situé dans /mips/messages/hhydrasys/phor_good/out.dat

from matplotlib import pyplot as plt
import numpy as np

with open("data.txt", 'r') as f:
    data = f.readline()

# j'ajoute un caractère '0' en début de chaine.
data = "0"+data

def get_groups(dat_str, by = 2):
    if len(dat_str) % by  != 0:
        print("IMPAIR")
        dat_str += "0"
    pairs = [dat_str[i:i+by] for i in range(0, len(dat_str), by)]
    return pairs

valeurs = []

group_by = 3
for i, valeur in enumerate(get_groups(data, by=group_by)):
    if i % group_by != 0 :
        decim = int(valeur, 16)
        print(decim)
        valeurs.append(decim)


x = range(len(valeurs))
y = valeurs


plt.plot(x,y)
plt.show(block=True)