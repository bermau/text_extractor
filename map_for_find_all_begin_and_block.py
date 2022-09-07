# Fichier pour la mise au point.
import lib_logstudy
from lib_logstudy import newline
i_file = r"data_in/demo_log_72_lines.log"

AA = lib_logstudy.TextManipulator(i_file)
AA.print_info()
AA.remove_carriage_return()
AA.cat()

newline()

select = AA.select_all_begin_end_block(init_pattern="Task start:", end_pattern="Executing task")




