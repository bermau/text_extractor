# Utilisation pour l'étude d'un log
import sys
import lib_logstudy
from lib_logstudy import display_lines

# import pandas as pd
sys.path.append("../HI_31_outils_divers")
from lib_bm_utils import readkey, title
# from utils_lib import title, _test, all_same_length, all_equal
# from lib_bm_utils import readkey, newname_for_file, input_int

i_file = r"./data_in/glimscron4_20220830_221610.log"



AA = lib_logstudy.TextManipulator(i_file, encoding="ANSI")
AA.remove_carriage_return()
# AA.cat()
print("Tail du fichier initial : ", len(AA))
title("Récupération de tous les 'Task Start'")
AA.select_regex("Task end")


# Créer une méthode pour extraire une sous chaine dans la regex
# AA.head(30)
# AA.cat()
title("Elimination début de ligne")

AA.replace_regex(r".* '", '')
# AA.cat()
AA.replace_regex(r"'", '')
title("La liste des CR à étudier")
AA.cat(quiet=True)
title ("Nombre de lignes " + str(len(AA)))

# Il faudrait récupérer une liste. Je crée l'outil adéquat AA.to_list()
list_des_cr = AA.to_list()
set_de_cr = set(list_des_cr)
title("Les CR activés sont donc...")
from pprint import pprint
pprint(set_de_cr)


print("leur nombre est de ", len(set_de_cr))




# Imprimer sans les numéros de lignes.
