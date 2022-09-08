#!/usr/bin/env python
# coding: utf-8


from dataclasses import dataclass

LIMITE_CARACTERES_LUS = 0  # pour debugger.
import re
import pdb


def display_lines(numbered_lines):
    if numbered_lines:
        if len(numbered_lines) == 1:
            print(numbered_lines[0][0], numbered_lines[0][1])
        else:
            for line in numbered_lines:
                if isinstance(line, NumberedLine):
                    print(line.num, line.text)
                else:
                    print(line[0], line[1], end='')


def mark_doubleline_block(numbered_lines):
    buf = [(0, "*" * 20 + "\n")]
    for i in numbered_lines:
        buf.append(i)
    buf.append((0, "*" * 20 + "\n"))
    return buf


def mark_line_block(numbered_lines):
    numbered_lines.append(NumberedLine(0, "*" * 20))
    return numbered_lines


def newline():
    print("*" * 30)


@dataclass
class NumberedLine:
    num: int
    text: str


class NumberedText:  # Unused ?
    def __init__(self, a_list_of_numbered_line):
        self.data = a_list_of_numbered_line

    def display(self):
        for line in self.data:
            print(line.num, line.text)


def get_imposer_marques(ligne='', positions=[], longueur=0):
    """renvoie la ligne 1 mise à la longueur et en remplaçant les caractères situés à la liste
     de positions par un caractère |
     ????
     """
    ligne = ligne.ljust(longueur)
    ligne_out = ''
    for i in range(len(ligne)):
        if i in positions:
            ligne_out = ligne_out + '|'
        else:
            ligne_out = ligne_out + ligne[i]
    return ligne_out


class TextManipulator:
    lines = []  # list of strings
    n_lines = []  # list of NumberedLine (nb, string)

    def __init__(self, filename=r"../input/*.csv", encoding="utf8"):  # Tested
        with open(filename, "r", encoding=encoding) as entree:
            self.lines = entree.readlines(LIMITE_CARACTERES_LUS)
        self.n_lines = [NumberedLine(num, text) for num, text in enumerate(self.lines, start=1)]

    def loadString(self, string):
        """"A string containing
    unix end of line will be separated in a list of strings"""
        self.lines = string.split("\n")

    def __len__(self):  # Tested
        return len(self.n_lines)

    def print_info(self):  # Tested
        print("Number of lines :  {}".format(len(self)))

    def head(self, n=5):  # Tested
        self.n_lines = self.n_lines[:n]

    def tail(self, n=5):  # Tested
        self.n_lines = self.n_lines[-n:]

    def slice(self, begin, end):  # Tested
        self.n_lines = self.n_lines[begin:end]

    def remove_regex(self, pattern, skip=0):  # Tested
        """Suppress lines containing a regex.
         modify self.n_lines"""
        p = re.compile(pattern)
        without_pattern = [line for line in self.n_lines[skip:] if not p.match(line.text)]
        self.n_lines = self.lines[0:skip]
        self.n_lines.extend(without_pattern)

    def replace_regex(self, pattern, repl, skip=0):  # Tested
        """Remplace un motif par un autre."""
        p = re.compile(pattern)
        replaced_pattern = [NumberedLine(line.num, p.sub(repl, line.text)) for line in self.n_lines[skip:]]
        # possible que cela soit plus rapide que :
        # sansPat=[re.sub(pattern,repl,line) for line in self.lignes[skip:]]
        self.n_lines = replaced_pattern
        # self.lines.extend(without_pattern)

    def select_regex(self, pattern, skip=0):  # Tested
        """Ne conserve que les lignes avec une RegEx."""
        p = re.compile(pattern)
        # avecPat = [line for line in self.lines if p.match(line)]
        with_pattern = [line for line in self.n_lines[skip:] if p.match(line.text)]
        self.n_lines = with_pattern

    def get_regex(self, pattern, skip=0):
        """retourne les lignes contenant une regex (sans toucher au n_lines)
        returns NumberedLines"""
        p = re.compile(pattern)
        with_pattern = [line for line in self.n_lines[skip:] if p.match(line.text)]
        return with_pattern

    def remove_empty_lines(self):  # tested
        without_empty_lines = [line for line in self.n_lines if (line.text != '\n' and line.text != '')]
        self.n_lines = without_empty_lines

    def remove_carriage_return(self):  # tested
        for line in self.n_lines:
            line.text = line.text.replace('\n', '')

    def remove_ff(self):  # NOT TESTED
        """Remove FF characters (hexadecimal 0C). Attention : python waits for 0C et returns 0c in lower case.
        In my experiment, there where FF et des FF followed by LF"""
        # Not tested !!
        sansFF = [line for line in self.n_lines if line.text not in ('\x0C\n', '\x0C')]
        self.n_lines = sansFF

    def formatEntete(self):
        """Insertion d'une entête expliquant les colonnes extraites"""

        ent = """NOM:Lot;Analyse;Debut;Fin	
cible;Moyenne;SD;CV
Type;Moyenne;SD;CV;Nb"""
        return ent

    def cat(self):  # tested
        # print(self.formatEntete())
        for line in self.n_lines:
            print(line.num, line.text)

    def writeFile(self, filename=r"./data_out/output.csv"):
        """Ecrit le résultat des lignes"""
        with open(filename, "w", encoding="latin1") as sortie:
            # sortie.write(self.formatEntete())
            sortie.write("\n")
            for line in self.n_lines:
                sortie.write(line.num, line.text + "\n")

    def writeFileForCSV(self, filename=r"../output/output.csv"):
        """Ecrit le résultat des lignes"""
        with open(filename, "w", encoding="latin1") as sortie:
            for line in self.lignesPourTableur:
                sortie.write(line + "\n")

    def containing(self, string):
        return [(line_nb, line) for line_nb, line in enumerate(self.lines) if string in line]

    def get_first_ocurence_with_contexte(self, string, skip_lines=0, before=0, after=0):  # tested
        for index, line in enumerate(self.n_lines[skip_lines:]):
            if string in line.text:
                return self.get_context(index + skip_lines, before, after)
        return None

    def generator_for_ocurence_with_contexte(self, string, start_line=0, before=0, after=0):

        compteur = start_line
        for line_nb, line in enumerate(self.lines[compteur:]):
            if string in line:
                compteur += line_nb
                yield self.get_context(line_nb, before, after)

    def find_all(self, string, start_line=0, before=0, after=0):
        gene = self.generator_for_ocurence_with_contexte(string=string, start_line=start_line, before=before,
                                                         after=after)
        buf = []
        for block in gene:
            if block:
                buf.extend(mark_line_block(block))
        print("*******************")
        display_lines(buf)
        print("*******************")

    def generator_for_begin_end_block(self, init_pattern, end_pattern, skip=0, before=0, after=0):  # Tested

        compteur = skip
        buffer = []
        status = 0
        for line_nb, numbered_line in enumerate(self.n_lines[skip:]):

            if status == 1:  # un début de block a déjà été trouvé :
                if end_pattern not in numbered_line.text:
                    buffer.append(numbered_line)
                else:  # On a trouvé le signal de fin
                    buffer.append(numbered_line)
                    status = 0
                    compteur += line_nb
                    yield buffer

            elif status == 0:  # En cours de recherche
                if init_pattern in numbered_line.text:
                    buffer = [numbered_line]
                    status = 1  # un début de block a été trouvé

    def get_all_begin_end_block(self, init_pattern, end_pattern, start_line=0,
                                before=0, after=0, mark_block=True):  # tested

        gene = self.generator_for_begin_end_block(init_pattern=init_pattern,
                                                  end_pattern=end_pattern,
                                                  skip=start_line, before=before, after=after)
        buf = []
        for block in gene:
            if block:
                if mark_block:
                    buf.extend(mark_line_block(block))
                else:
                    buf.extend(block)
        print("***************************************")
        display_lines(buf)
        print("***************************************")
        return buf

    def select_all_begin_end_block(self, *args, **kwargs):
        """Idem as get_  but modify self.n_lines"""
        select = self.get_all_begin_end_block(*args, **kwargs)
        self.n_lines = select

    def debut_fin_first(self, init_pattern, end_pattern):
        status = 0
        buffer = []

        for line_nb, line in enumerate(self.lines):
            if status == 1:  # déjà trouvé :
                if end_pattern not in line:
                    buffer.append((line_nb, line))
                else:
                    buffer.append((line_nb, line))
                    status = 2
                    break
            if status == 0:
                if init_pattern in line:
                    buffer.append((line_nb, line))
                    status = 1
        return buffer

    def get_context(self, idx, before, after):
        """Retourne une ligne avec son contexte depuis self.n_lines"""
        buffer = []
        return self.n_lines[idx - before:idx + after + 1]
