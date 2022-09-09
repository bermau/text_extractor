# Utilisation : Quel sont les commandes productives ?

import sys
import lib_logstudy
from lib_logstudy import display_lines
from pprint import pprint
import glob
# Vers la ligne 21634,il y a une suite d'impression.


# import pandas as pd
sys.path.append("../HI_31_outils_divers")
from lib_bm_utils import readkey, title

default_file = r"./data_in/glimscron4_20220830_221610.log"

def traitement(i_file = default_file):
    title ("Etude du log de "+ i_file)
    AA = lib_logstudy.TextManipulator(i_file, encoding="ANSI")
    AA.remove_carriage_return()
    # AA.cat()
    print("Taille du fichier initial est : ", len(AA))
    title("Récupération de tous les 'Task Start'")

    AA.select_all_begin_end_block("Task start", "Task end")
    AA.slice(15000, 15500)
    AA.cat()
    print("Rescriction à lignes ", len(AA))
    #
    # # Créer une méthode pour extraire une sous chaine dans la regex
    # # AA.head(30)
    # # AA.cat()
    # # title("Elimination début de ligne")
    #
    # AA.replace_regex(r".* '", '')
    # # AA.cat()
    # AA.replace_regex(r"'", '')
    # # title("La liste des CR à étudier")
    # # AA.cat(quiet=True)
    # title ("Nombre de lignes " + str(len(AA)))
    #
    # # Il faudrait récupérer une liste. Je crée l'outil adéquat AA.to_list()
    # list_des_cr = AA.to_list()
    # set_de_cr = set(list_des_cr)
    #
    # title("Les CR activés sont donc...")
    # pprint(set_de_cr)
    #
    # print("leur nombre est de ", len(set_de_cr))
    #
    readkey("t...")

if __name__ == '__main__':

    traitement()
# BOUCLE
    lst_fichiers_a_traiter  = sorted(glob.glob("./data_in/glims*.log"))
    pprint(lst_fichiers_a_traiter)

    for file in lst_fichiers_a_traiter:
        traitement(file)


# Imprimer sans les numéros de lignes.
