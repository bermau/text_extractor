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
# AA.get_all_begin_end_block(init_pattern="Task start:", end_pattern="Executing task")
# AA.supRegex("0 ")
# AA.supp_empty_lines()
AA.remove_carriage_return()
AA.cat()
new_line()

print("Tests de : remove_regex")
AA.replace_regex("ceci", "cela")
AA.cat()

# AA.cat()
# AA.print_info()

