#!/usr/bin/env python
# coding: utf-8

# Etude log commandes d'impression.
# 
# Je veux savoir quelles sont les Modèles de CR utilisés en 2022.
# J'ai récupéré les logs de glimscron4.

import pdb

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


class TextManipulator:

    def __init__(self, file):
        f = open(file)
        self.lines = f.readlines()
        f.close()

    def print_info(self):
        print("Number of lines :  {}".format(len(self.lines)))

    def containing(self, string):
        return [(line_nb, line) for line_nb, line in enumerate(self.lines) if string in line]

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

