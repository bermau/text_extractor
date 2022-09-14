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


# Essai de modification d'une fonction à la classe TextManipulator
def get_all_begin_end_block(self, init_pattern, end_pattern, start_line=0,
                            before=0, after=0, mark_block=True):  # tested

    gene = self.generator_for_begin_end_block(init_pattern=init_pattern,
                                              end_pattern=end_pattern,
                                              skip=start_line, before=before, after=after)
    buf = []
    for block in gene:
        if len(block) != 7:  # NOUVEAU
            # On va créer un sous-objet
            # keep only the first line of the block
            block_a_enregistrer = [block[0]]
            block_obj = TextManipulator(block)
            info = "Bloc de {} lignes".format(len(block_obj))
            block_obj.select_regex(".*/messages")
            # block_obj.cat()
            block_lines = block_obj.to_list(quiet=False)
            block_ln = len(block_obj)
            info += " {} messages".format(block_ln)
            info_avec_num = NumberedLine(0, info)
            block_a_enregistrer.extend([info_avec_num])
            block_a_enregistrer.extend(block_lines)
            if mark_block:
                buf.extend(mark_line_block(block_a_enregistrer))
            else:
                buf.extend(block_a_enregistrer)
    return buf


lib_logstudy.TextManipulator.get_all_begin_end_block = get_all_begin_end_block


def simple_action_on_block(block):
    return block


def traitement(i_file=default_file):
    title("Etude du log de " + i_file)
    AA = lib_logstudy.TextManipulator(i_file, encoding="latin1")
    AA.remove_carriage_return()
    # AA.cat()
    print("Taille du fichier initial est : ", len(AA))
    title("Récupération de tous les 'Task Start'")

    # AA.select_all_begin_end_block("Task start", "Task end")
    # AA.sce(15000, 15500)
    # AA.select_lines(21634, 21700)

    # AA.head(50)
    print()
    # AA.cat()
    # readkey("t...")

    title("Etape 2 : généré commande | nombre de documents générés")

    AA.select_all_begin_end_block(init_pattern="Task start", end_pattern=".*message", start_line=0,
                                  before=0, after=0, mark_block=True, block_action=simple_action_on_block  # Tested

                                  )

    # AA.find_all("Task start", before = 0, after = 1)
    AA.cat()


if __name__ == '__main__':
    traitement()
# BOUCLE
#     lst_fichiers_a_traiter  = sorted(glob.glob("./data_in/glims*.log"))
#     pprint(lst_fichiers_a_traiter)
#
#     for file in lst_fichiers_a_traiter:
#         traitement(file)


# Imprimer sans les numéros de lignes.
