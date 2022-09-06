# Fichier pour la mise au point.
import log_study

i_file = r"./data_in/very_short.log"


AA = log_study.TextManipulator(i_file)
AA.print_info()

AA.find_all_begin_end_block(init_pattern="Task start:", end_pattern="Executing task")


