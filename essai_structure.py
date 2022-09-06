from dataclasses import dataclass
import re


LIMITE_CARACTERES_LUS = 10000
@dataclass
class NumberedLine:
    num: int
    text: str

class TextManipulator:
    lines = [] # list of strings
    n_lines = [] # list of NumberedLine (nb, string)

    def __init__(self, filename=r"../input/*.csv", encoding="utf8"):
        with open(filename, "r", encoding=encoding) as entree:
            self.lines = entree.readlines(LIMITE_CARACTERES_LUS)
        self.n_lines = [NumberedLine(num, line) for num, line in enumerate(self.lines, start=1)]
        print("Number of initial lines :  {}".format(len(self.n_lines)))

    def print_info(self):
        print("Number of lines :  {}".format(len(self.n_lines)))




    def sup_regex(self, pattern):
        """Supprime les lignes contenant une RegEx.
- modifie self.n_lines"""

        p = re.compile(pattern)
        without_pattern = [(line.num, line.text) for line in self.n_lines if not p.match(line.text)]
        self.n_lines = without_pattern

if __name__ == '__main__':
    AA  = TextManipulator("short_demo_log.log")
    AA.print_info()
    AA.sup_regex("ceci")
    AA.print_info()
