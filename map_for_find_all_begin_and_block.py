# Fichier pour la mise au point.
import lib_logstudy

i_file = r"data_in/demo_log_72_lines.log"

AA = log_study.TextManipulator(i_file)
AA.print_info()

AA.find_all_begin_end_block(init_pattern="Task start:", end_pattern="Executing task")


