#!/usr/bin/env python
# coding: utf-8

# Etude log commandes d'impression.
# 
# Je veux savoir quelles sont les Modèles de CR utilisés en 2022.
# J'ai récupéré les logs de glimscron4.
from dataclasses import dataclass

LIMITE_CARACTERES_LUS = 0  # pour debugger.
import re
import pdb

def display_lines(numbered_lines):
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
    numbered_lines.append((0, "*" * 20 + "\n"))
    return numbered_lines

@dataclass
class NumberedLine:
    num: int
    text: str

class NumberedText:
    def __init__(self, a_list_of_numbered_line):
        self.data = a_list_of_numbered_line
    def display(self):
        for line in data:
            print(data.int, data.text)

class TextManipulator:

    lines = [] # list of strings
    n_lines = [] # list of NumberedLine (nb, string)

    def __init__(self, filename=r"../input/*.csv", encoding="utf8"):
        with open(filename, "r", encoding=encoding) as entree:
            self.lines = entree.readlines(LIMITE_CARACTERES_LUS)
        self.n_lines = [NumberedLine(num, text) for num, text in enumerate(self.lines, start=1)]
        print("Number of initial lines :  {}".format(len(self.n_lines)))


    def loadString(self, string):
            """"A string containing
    unix end of line will be separated in a list of strings"""
            self.lines = string.split("\n")

    def __len__(self):
        return len(self.n_lines)

    def print_info(self):
        print("Number of lines :  {}".format(len(self)))

    def head(self, n=5):
        self.n_lines = self.n_lines[:n]

    def tail(self, n=5):
        self.n_lines = self.n_lines[-n:]

    def slice(self, begin, end):
        self.n_lines = self.n_lines[begin:end]

    def sup_regex(self, pattern, skip=0):
        """Suppress lines containing a regex.
         modify self.n_lines"""
        p = re.compile(pattern)
        without_pattern = [line for line in self.n_lines[skip:] if not p.match(line.text)]
        self.n_lines = self.lines[0:skip]
        self.n_lines.extend(without_pattern)


    def replace_regex(self, pattern, repl, skip=0):
        """Remplace un motif par un autre"""
        p = re.compile(pattern)
        replaced_pattern = [p.sub(repl, line.text) for line in self.n_lines[skip:]]
        # possible que cela soit plus rapide que :
        # sansPat=[re.sub(pattern,repl,line) for line in self.lignes[skip:]]
        self.n_lines = replaced_pattern
        # self.lines.extend(without_pattern)

    def select_regex(self, pattern, skip=0):
        """Ne conserve que les lignes avec une RegEx."""
        p = re.compile(pattern)
        # avecPat = [line for line in self.lines if p.match(line)]
        with_pattern = [line for line in self.n_lines[skip:] if p.match(line.text)]
        self.n_lines = with_pattern


    def get_regex(self, pattern, skip=0):
        """retourne les lignes contenant une regex"""
        p = re.compile(pattern)
        avecPat = [line for line in self.lines[skip:] if p.match(line)]
        return avecPat

    def remove_empty_lines(self):
        # print(mapage)
        without_empty_lines = [line for line in self.n_lines if line.text != '\n']
        self.n_lines = without_empty_lines

    def remove_carriage_return(self):
        for line in self.n_lines:
            line.text = line.text.replace('\n', '')

    def suppFF(self):
        """supprime les caractères FF (hexadécimal 0C). Attention python attent 0C et retourne avec un 0c en minuscule.
        Dans le cas présent, il a des FF et des FF suivis de LF"""
        sansFF = [line for line in self.n_lines if line.text not in ('\x0C\n', '\x0C')]
        self.n_lines = sansFF

    def get_imposer_marques(self, ligne='', positions=[], longueur=0):
        """renvoie la ligne 1 mise à la longueur et en remplaçant  les caractères situés à la liste de positions par un caractère |"""
        ligne = ligne.ljust(longueur)
        ligne_out = ''
        for i in range(len(ligne)):
            if i in positions:
                ligne_out = ligne_out + '|'
            else:
                ligne_out = ligne_out + ligne[i]
        return ligne_out

    def traitementSpecifique(self):
        """ Ce traitement est écrit d'une façon sans doute peu efficace, mais il fonctionne.
"""
        condition = r'^PCC.*'
        pat = re.compile(condition)
        lignesOut = []
        titre = ''
        for item in self.n_lines:
            if pat.match(item.text):
                # self.lignesOut.append(item)
                titre = item.text + ';'
            else:
                lignesOut.append(titre + item.text)
        self.n_lines = lignesOut

    def formatEntete(self):
        """Insertion d'une entête expliquant les colonnes extraites"""

        ent = """NOM:Lot;Analyse;Debut;Fin	
cible;Moyenne;SD;CV
Type;Moyenne;SD;CV;Nb"""
        return ent

    def cat_lines(self):
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

    def getVirgulesPointVirgules():
        """Retour le nombre virgules et points virgules de l'entrée. Cela
permet de vérifier le type de séparateur utilisé"""

    def containing(self, string):
        return [(line_nb, line) for line_nb, line in enumerate(self.lines) if string in line]

    def first_ocurence(self, string):
        for line in self.n_lines:
            if string in line.text:
                return [line]

    def get_first_ocurence_with_contexte(self, string, skip_lines=0, before=0, after=0):
        for index, line in enumerate(self.n_lines[skip_lines:]):
            if string in line.text:
                return self.context(index + skip_lines, before, after)
        return None

    def generator_for_ocurence_with_contexte(self, string, start_line=0, before=0, after=0):

        compteur = start_line
        for line_nb, line in enumerate(self.lines[compteur:]):
            if string in line:
                compteur += line_nb
                yield self.context(line_nb, before, after)

    def find_all(self, string, start_line=0, before=0, after=0):
        gene = self.generator_for_ocurence_with_contexte(string=string, start_line=start_line, before=before, after=after)
        buf = []
        for block in gene:
            if block:
                buf.extend(mark_line_block(block))
        print("*******************")
        display_lines(buf)
        print("*******************")

    def generator_debut_fin(self, init_pattern, end_pattern, start_line=0, before=0, after=0):

        compteur = start_line
        buffer = []
        status = 0
        for line_nb, line in enumerate(self.lines[start_line:]):

            if status == 1:  # un début de block a déjà été trouvé :
                if end_pattern not in line:
                    buffer.append((line_nb, line))
                else:  # On a trouvé le signal de fin
                    buffer.append((line_nb, line))
                    status = 0
                    compteur += line_nb
                    yield buffer

            elif status == 0: # En cours de recherche
                if init_pattern in line:
                    buffer = [(line_nb, line)]
                    status = 1  # un début de block a été trouvé



    def find_all_begin_end_block(self, init_pattern, end_pattern, start_line=0, before=0, after=0):
        gene = self.generator_debut_fin(init_pattern=init_pattern, end_pattern=end_pattern,
                                        start_line=start_line, before=before, after=after)
        buf = []
        for block in gene:
            if block:
                buf.extend(mark_line_block(block))
        print("***************************************")
        display_lines(buf)
        print("***************************************")

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

    def context(self, idx, before, after):
        """Retourne une ligne avec son contexte depuis self.n_lines"""
        buffer = []
        return self.n_lines[idx-before:idx+after+1]
        # for i in range(idx - before, idx + after+1):
        #     if self.n_lines[i]:
        #         buffer.append((i, self.n_lines[i]))
        # return buffer

