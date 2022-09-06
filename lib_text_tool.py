#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# text_tool.py
""" Ce programme traite des fichiers textes ou des textes.
"""
LIMITE_CARACTERES_LUS = 0  # pour debugger.
import pdb, re


def display_lines(numbered_lines):
    if len(numbered_lines) == 1:
        print(numbered_lines[0][0], numbered_lines[0][1])
    else:
        for line in numbered_lines:
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


class TextManipulator():
    """Ouvre un fichier et élimine tout ce qui ne convient pas.
        Ecrit une copie"""
    lignesPourTableur = []
    lines = []

    def __init__(self, filename=r"../input/*.csv", encoding="utf8"):
        with open(filename, "r", encoding=encoding) as entree:
            self.lines = entree.readlines(LIMITE_CARACTERES_LUS)
        print("Number of initial lines :  {}".format(len(self.lines)))

    def loadString(self, string):
        """"A string containing
unix end of line will be separated in a list of strings"""
        self.lines = string.split("\n")

    def print_info(self):

        print("Number of lines :  {}".format(len(self.lines)))

    def supRegex(self, pattern):
        """Supprime les lignes contenant une RegEx.

- modifie self.lignes"""
        p = re.compile(pattern)
        sansPat = [line for line in self.lines if not p.match(line)]
        self.lines = sansPat

    def imposeRegex(self, pattern):
        """Ne conserve que les lignes avec une RegEx."""
        p = re.compile(pattern)
        avecPat = [line for line in self.lines if p.match(line)]
        self.lines = avecPat

    def supRegexSkiping(self, pattern, skip=0):
        p = re.compile(pattern)
        sansPat = [line for line in self.lines[skip:] if not p.match(line)]
        self.lines = self.lines[0:skip]
        self.lines.extend(sansPat)

    def remplacerRegex(self, pattern, repl, skip=0):
        """Remplace un motif par un autre"""
        p = re.compile(pattern)
        without_pattern = [p.sub(repl, line) for line in self.lines[skip:]]
        # possible que cela soit plus rapide que :
        # sansPat=[re.sub(pattern,repl,line) for line in self.lignes[skip:]]

        self.lines = self.lines[0:skip]
        self.lines.extend(without_pattern)

    def find_regex(self, pattern, skip=0):
        """Affiche les lignes contenant une regex"""
        p = re.compile(pattern)
        avecPat = [line for line in self.lines[skip:] if p.match(line)]
        for line in avecPat:
            print(line)

    def getRegex(self, pattern, skip=0):
        """retourne les lignes contenant une regex"""
        p = re.compile(pattern)
        avecPat = [line for line in self.lines[skip:] if p.match(line)]
        return avecPat

    def supp_empty_lines(self):
        # print(mapage)
        without_empty_lines = [line for line in self.lines if line != '\n']
        self.lines = without_empty_lines

    def suppRetourLignes(self):
        """Atention a éventuel effet de bord"""
        self.lines = [self.lines[i].replace('\n', '') for i in range(len(self.lines))]

    def suppFF(self):
        """supprime les caractères FF (hexadécimal 0C). Attention python attent 0C et retourne avec un 0c en minuscule. 
        Dans le cas présent, il a des FF et des FF suivis de LF"""
        sansFF = [line for line in self.lines if line not in ('\x0C\n', '\x0C')]
        self.lines = sansFF

    def first_ocurence(self, string):
        for line_nb, line in enumerate(self.lines):
            if string in line:
                return [(line_nb, line)]

    def first_ocurence_with_contexte(self, string, start_line=0, before=0, after=0):
        for line_nb, line in enumerate(self.lines[start_line:]):
            if string in line:
                return self.context(line_nb + start_line, before, after)

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

    def context(self, line_number, before, after):
        """Retourne une ligne avec son contexte."""
        buffer = []
        for i in range(line_number - before, line_number + after + 1):
            if self.lines[i]:
                buffer.append((i, self.lines[i]))
        return buffer




    def imposerMarques(self, ligne='', positions=[], longueur=0):
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
        self.lignesOut = []
        titre = ''
        for item in self.lines:
            if pat.match(item):
                # self.lignesOut.append(item)
                titre = item + ';'
            else:
                self.lignesOut.append(titre + item)
        self.lines = self.lignesOut

    def formatEntete(self):
        """Insertion d'une entête expliquant les colonnes extraites"""

        ent = """NOM:Lot;Analyse;Debut;Fin	
cible;Moyenne;SD;CV
Type;Moyenne;SD;CV;Nb"""
        return ent

    def cat_lines(self):
        # print(self.formatEntete())
        for line in self.lines:
            print(line)

    def writeFile(self, filename=r"./data_out/output.csv"):
        """Ecrit le résultat des lignes"""
        with open(filename, "w", encoding="latin1") as sortie:
            # sortie.write(self.formatEntete())
            sortie.write("\n")
            for line in self.lines:
                sortie.write(line + "\n")

    def writeFileForCSV(self, filename=r"../output/output.csv"):
        """Ecrit le résultat des lignes"""
        with open(filename, "w", encoding="latin1") as sortie:
            for line in self.lignesPourTableur:
                sortie.write(line + "\n")

    def getVirgulesPointVirgules():
        """Retour le nombre virgules et points virgules de l'entrée. Cela
permet de vérifier le type de séparateur utilisé"""


if __name__ == '__main__':
    net = TextManipulator()
    net.read_file(filename="./data_in/very_short.log", encoding="latin1")
    net.suppRetourLignes()
    net.cat_lines()
    net.supp_empty_lines()
    # net.supRegexSkiping(".*scheduler", skip=0)
    net.supRegexSkiping("12625")
    net.supRegex(r".*private.*|.*CR.*")
    net.print_info()
    net.cat_lines()
    # net.remplacerRegex(r';{2,}',r';') # remplacer les suites de plus de 2 ; par un seul.^^
    # net.remplacerRegex(r'^;',r'') # supp ; de début
    # net.remplacerRegex(r';$',r'') # supp ; de de fin
    # net.remplacerRegex(r'\.',r',')# virgule française
    # net.remplacerRegex(r'Condition du ',r'') #
    # net.remplacerRegex(r' au ',r';') #
    # net.remplacerRegex(r' : ',r';') # pour récupérer les num de lot
    # net.remplacerRegex(r' - ',r';') # pour récupérer les num de lot
    # net.supRegex(r'^[;]*$') # chaîne ne contenant que des ;
    # # la lignes suivante recherche les lignes constituées uniquement de chiffres, espace et , entre le début et la fin.
    # net.remplacerRegex(r'^([1234567890, ;]*)$', r'Cible;\1')
    # # Il reste à copier l'entête de chaque groupe entre début de colonne... mais la taille du groupe est irrégulier.
    # net.traitementSpecifique()
    # net.formatEntete()
    # net.catLignes()
    net.writeFile("./data_out/sortie.txt")
