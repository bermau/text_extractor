

@dataclass
class NumberedLine:
    num: int
    text: str


class TextManipulator
    lines = [] # list of strings
    n_lines = [] # list of NumberedLine (nb, string)

    def __init__(self, filename=r"../input/*.csv", encoding="utf8"):
        with open(filename, "r", encoding=encoding) as entree:
            self.lines = entree.readlines(LIMITE_CARACTERES_LUS)
        self.n_lines = [NumberedLine(num, line) for num, line in enumerate(self.lines, start=1)]
        print("Number of initial lines :  {}".format(len(self.n_lines)))
