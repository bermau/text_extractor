# Utilisation : Quel sont les commandes productives ?

import sys
import lib_logstudy

from lib_logstudy import display_lines, mark_line_block, TextManipulator, NumberedLine
from pprint import pprint
import glob

# Vers la ligne 21634,il y a une suite d'impression.


# import pandas as pd

sys.path.append("../HI_31_outils_divers")
from lib_bm_utils import readkey, title

default_file = r"./data_in/glimscron4_20220830_221610.log"




def action_on_main_block(block):
    """Return the number of lines, then the lines"""
    buf = []
    if len(block) != 7:
        # On va créer un sous-objet : block_obj
        # keep only the first line of the block
        block_a_enregistrer = [block[0]]

        block_obj = TextManipulator(block)
        info = "Bloc de {} lignes, contentant".format(len(block_obj))
        block_obj.select_regex(".*/messages")
        # block_obj.cat()
        block_lines = block_obj.to_list(quiet=False)
        block_ln = len(block_obj)
        info += " {} messages".format(block_ln)
        info_avec_num = NumberedLine(0, info)
        block_a_enregistrer.extend([info_avec_num])
        block_a_enregistrer.extend(block_lines)
        buf.extend(block_a_enregistrer)

    return  buf


def no_action_on_block(block):
    """Just to test signature"""
    return block

def main(i_file=default_file):
    title("Etude du log de " + i_file)
    AA = lib_logstudy.TextManipulator(i_file, encoding="latin1")
    AA.remove_carriage_return()
    # AA.cat()
    print("Taille du fichier initial est : ", len(AA))
    title("Récupération de tous les 'Task Start'")

    AA.select_all_begin_end_block("Task start", "Task end",
                                  # mark_block=False,
                                  block_action=action_on_main_block)

    # AA.select_lines(21174, 21174 + 300)

    # AA.head(500)
    print()
    AA.cat()
    readkey("t...")

    title("Etape 2 : généré commande | nombre de documents générés")
    #
    # AA.select_all_begin_end_block(init_pattern="Task start", end_pattern=".*message", start_line=0,
    #                               before=0, after=0, mark_block=True, block_action=simple_action_on_block  # Tested
    #                               )

    # AA.find_all("Task start", before = 0, after = 1)
    AA.cat()


if __name__ == '__main__':
    main()
# BOUCLE
#     lst_fichiers_a_traiter  = sorted(glob.glob("./data_in/glims*.log"))
#     pprint(lst_fichiers_a_traiter)
#
#     for file in lst_fichiers_a_traiter:
#         traitement(file)


# Imprimer sans les numéros de lignes.
