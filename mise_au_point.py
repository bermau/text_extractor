# Fichier pour la mise au point.
import lib_text_tool

i_file = r"./data_in/very_short.log"


AA = lib_text_tool.TextManipulator(i_file)
AA.print_info()

AA.find_all_begin_end_block(init_pattern="Task start:", end_pattern="Executing task")
AA.supRegex("0 ")
AA.supp_empty_lines()
AA.cat_lines()
AA.print_info()

