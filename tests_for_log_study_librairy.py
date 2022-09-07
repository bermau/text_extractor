# this file contains tests to validate my librairy

from lib_logstudy import *

i_file = r"data_in/demo_log_10_fictive_lines.log"

AA = TextManipulator(i_file)
print('***** first_ocurence *****')
AA.first_ocurence("ceci")

# display_lines(mark_line_block(AA.first_ocurence_with_contexte("ceci",   3,3)))
# print('**********')
# mark_line_block(AA.first_ocurence_with_contexte("/mips/messag",   3,3))
# print('**********')
# display_lines(AA.first_ocurence("L22126808"))
# print('**********')
# display_lines(mark_line_block(AA.first_ocurence_with_contexte("/mips/messag", start_line=400)))
# print('**********')
# AA.first_ocurence_with_contexte("/mips/messag", 3,3)
# print('**********')
# mark_line_block(AA.first_ocurence_with_contexte("/mips/messag", 3,3))
# display_lines(mark_line_block(AA.next_ocurence_with_contexte("/mips/messag", start_line=400)))