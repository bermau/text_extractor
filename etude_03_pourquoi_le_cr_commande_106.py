# Utilisation : Quel sont les commandes productives ?
# A quoi sert la commande 106 '106 - CR_LABO_Complet_EXTERNE'
# elle ne semble pas produire de PDF stockés... mais elle est sans doute à l'origine des impressions directes
#  '105 - CR_LABO_Complet'                0 production de pdf
#  '106 - CR_LABO_Complet_EXTERNE'        0 production de pdf
# '110 - CR_Microbio_Complet'   qui sebme totalement abandonné
import os.path
import sys
import lib_logstudy
import re
import pandas as pd

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

def summary_of_block(block):
    """Un résumé du block en une ligne"""
# Exemple de block :
# 42552 Task start: 31/08/2022 17:36:13 '107 - CR_LABO_Complet PDF'
# 0 Bloc de 155 lignes, contentant 24 messages

    buf = []
    if block != []:
        first_line=  block[0].text
        line1 = first_line[first_line.index(" '"):]

        extract = re.search(r"(\d+) lignes.* (\d+) messages", block[1].text)
        buf.append(NumberedLine(block[0].num,"\t".join([line1, extract.groups()[0], extract.groups()[1]] )))
    return buf

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

    AA.select_all_begin_end_block("Task start.*'110 - CR_Microbio_Complet'", "Task end",
                                  # mark_block=False,
                                  block_action=action_on_main_block)

    # AA.select_lines(21174, 21174 + 300)
    print()
    AA.cat()

    title("Retirer les marques de bloc, faire résumé en une ligne")
    AA.select_all_begin_end_block("Task start", "****", mark_block=False, block_action=summary_of_block)
    AA.cat()
    print("Nombre de lignes", str(len(AA)))
    # On va trier les lignes avec pandas, qui accepte des listes de listes
    df_aa = pd.DataFrame(AA.to_list_of_list(quiet=False).copy(), columns=['num', 'text'])
    df_bb = df_aa.sort_values(by='text')
    print(df_bb)       # OK
    # soit sort df_bb sur un fichier, soit on crée un TextManipulator
    print(df_bb.values.tolist())

    BB = lib_logstudy.TextManipulator(df_bb.values.tolist(), encoding="latin1") # OK sous Linux

    BB.cat()
    BB.writeFile(os.path.join("./data_out","sortie_"+os.path.basename(i_file)+'.csv'))
    file_name = os.path.join("./data_out", "sortie_" + os.path.basename(i_file) + '.csv')
    print("Sortie des données sur ", file_name)
    BB.writeFile(file_name)

if __name__ == '__main__':
    main()



# # BOUCLE
#     lst_fichiers_a_traiter  = sorted(glob.glob("./data_in/glims*.log"))
#     pprint(lst_fichiers_a_traiter)
#
#     for file in lst_fichiers_a_traiter:
#         main(file)
#         input("Key to continue...")

