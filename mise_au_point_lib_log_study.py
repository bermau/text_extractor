# Fichier pour la mise au point.
import lib_logstudy
from lib_logstudy import display_lines

# i_file = r"./data_in/glimscron4_20220830_221610.log"
i_file = r"./data_in/demo_log_10_fictive_lines.log"

def new_line():
    print("*" * 30)


AA = lib_logstudy.TextManipulator(i_file, encoding="utf-8")

AA.print_info()

#
# AA.find_all_begin_end_block(init_pattern="Task start:", end_pattern="Executing task")
# AA.supRegex("0 ")
# AA.supp_empty_lines()
AA.remove_carriage_return()
AA.cat_lines()
# AA.get_first_ocurence_with_contexte("Dossier 20141709", before=2, after= 3)
# Cette recherche ne ramène rien.
print("Tests de : get_first_ocurence_with_contexte('Dossier 20141709'', before=2, after= 3)")
display_lines(AA.get_first_ocurence_with_contexte("Dossier 20141709", before=2, after= 3))

new_line()


print("Tests de : sup_regex")
AA.replace_regex("ceci", "cela")
AA.cat_lines()

# AA.cat_lines()
# AA.print_info()

