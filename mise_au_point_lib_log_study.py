# Fichier pour la mise au point.
import lib_text_tool

i_file = r"./data_in/glimscron4_20220830_221610.log"

AA = lib_text_tool.TextManipulator(i_file, encoding="ANSI")

# AA.print_info()
#
# AA.find_all_begin_end_block(init_pattern="Task start:", end_pattern="Executing task")
# AA.supRegex("0 ")
# AA.supp_empty_lines()
AA.remove_carriage_return()
AA.find_all_begin_end_block("Task start", "INFO")

AA.cat_lines()
AA.print_info()

