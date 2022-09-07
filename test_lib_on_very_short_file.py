import unittest
from unittest.mock import patch

import lib_logstudy
from lib_logstudy import display_lines

i_file = r"data_in/demo_log_10_fictive_lines.log"

def greet(name):
    print('Hello ', name)

def new_line():
    print("*" * 30)

class CalculsTest(unittest.TestCase):
    """Cette classe contient les méthodes qui, si elles conmmencent par le mot
test, sont des tests unitaires."""

    @classmethod
    def setUpClass(self):
        print("SetUp class environment")

    def setUp(self):
        print("    SetUp environment")
        self.AA = lib_logstudy.TextManipulator(i_file, encoding='UTF-8')

    def tearDown(self):
        print("    Tearing down environment.\n")

    def test_toujours_vrai(self):
        """.....Test toujours vrai """
        print("Test toujours vrai")
        self.assertTrue(True)

    @patch('builtins.print')
    def test_greet(self, mock_print):
        # The actual test
        greet('John')
        mock_print.assert_called_with('Hello ', 'John')
        greet('Eric')
        mock_print.assert_called_with('Hello ', 'Eric')

    @patch('builtins.print')
    def test_printinfo(self, mock_print):
        self.AA.print_info()
        mock_print.assert_called_with("Number of lines :  9")

    def test_len(self):
        print("Test de len")
        self.assertEqual(len(self.AA.n_lines), 9)

    def test_head(self):
        self.AA.remove_carriage_return()
        self.AA.head(3)
        self.AA.cat_lines()
        self.assertEqual(self.AA.n_lines[-1].text, 'et voici sa fin sur la ligne 3')

    def test_tail(self):
        self.AA.remove_carriage_return()
        self.AA.tail(3)
        self.AA.cat_lines()
        self.assertEqual(self.AA.n_lines[-1].text, 'et voici sa fin. La fin est sur la ligne 9.')
        self.assertEqual(len(self.AA), 3)

    def test_tail_head_slice(self):
        self.AA.remove_carriage_return()
        self.AA.tail(7) # 3456789
        self.AA.head(6) # 345678
        self.AA.slice(2, 4) # 56
        self.AA.cat_lines()
        self.assertTrue(self.AA.n_lines[-1].text.endswith("la ligne 6"))
        self.assertEqual(len(self.AA), 2)

    def test_seq(self):
        self.AA.remove_carriage_return()
        self.AA.head(3)
        self.AA.cat_lines()
        self.assertEqual(self.AA.n_lines[-1].text, 'et voici sa fin sur la ligne 3')

    def test_zz_sequence_1(self):
        print("Test de seq 1")
        self.AA.remove_carriage_return()
        rep = self.AA.get_first_ocurence_with_contexte("Dossier 20141709", before=2, after=3)
        self.assertEqual(rep, None)

    def test_get_first_ocurence_with_contexte(self):
        print("Test de get_first_ocurence_with_contexte")
        self.AA.remove_carriage_return()
        rep = self.AA.get_first_ocurence_with_contexte("ligne", before=1, after=1)
        self.AA.cat()
        print(rep)
        self.assertEqual(len(rep), 3)



    def test_remove_regex(self):
        print("Test de remove_regex complexe")
        self.AA.remove_carriage_return()
        self.AA.remove_regex(".*2020")
        self.AA.remove_regex('-----|Executing')
        self.assertEqual(len(self.AA), 9)

    def test_remove_regex_2(self):
        print("Test de remove_regex simple")
        self.AA.remove_carriage_return()
        self.AA.remove_regex(".*ceci")
        self.AA.cat_lines()
        new_line()
        self.AA.remove_regex(".*para")
        self.AA.cat_lines()
        self.assertEqual(len(self.AA), 3)

    def test_select_regex(self):
        print("Test de select_regex : On doit trouver 4 lignes avec le mot fin")
        self.AA.remove_carriage_return()
        self.AA.select_regex(".*fin")
        self.assertEqual(len(self.AA), 4)
        self.AA.cat_lines()

    def test_replace_regex(self):
        print("Test pour replace_regex : remplacer ceci par cela puis supprimer cela. Restent 6 lignes")
        self.AA.remove_carriage_return()
        self.AA.replace_regex("ceci", "cela")
        self.AA.cat_lines()
        new_line()
        self.AA.remove_regex("cela")
        self.AA.cat_lines()
        self.assertEqual(self.AA.n_lines[-1].num, 9)
        self.assertEqual(len(self.AA), 6)

    def test_get_regex(self):
        print("Test de get_regex : Selectionner les ligne contenant fin")
        self.AA.remove_carriage_return()
        self.AA.cat_lines()
        new_line()
        selection_of_numberedlines = self.AA.get_regex(".*fin")
        self.assertEqual(len(selection_of_numberedlines), 4)
        self.assertEqual(selection_of_numberedlines[2].num, 7)

    def test_get_context(self):
        self.AA.remove_carriage_return()
        select = self.AA.get_context(4,1,0)
        self.AA.cat()
        new_line()
        display_lines(select)
        self.assertEqual(len(select),2)
        self.assertEqual(select[0].num, 4)

def test_suite():
    """Retourne la liste des tests à traiter."""
    tests = [unittest.makeSuite(CalculsTest)]
    return unittest.TestSuite(tests)


if __name__ == '__main__':
    """Programme de test de vérification."""
    # lancer les unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(CalculsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)