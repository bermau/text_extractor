import unittest
from unittest.mock import patch

import lib_log_study
from lib_log_study import display_lines

i_file = r"data_in/demo_log_10_fictive_lines.log"

def greet(name):
    print('Hello ', name)

class CalculsTest(unittest.TestCase):
    """Cette classe contient les méthodes qui, si elles conmmencent par le mot
test, sont des tests unitaires."""

    @classmethod
    def setUpClass(self):
        print("SetUp class environment")

    def setUp(self):
        print("SetUp environment")
        self.AA = lib_log_study.TextManipulator(i_file, encoding='UTF-8')

    def tearDown(self):
        print("Tearing down environment.\n")

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
        self.assertEqual(len(rep), 6)
        self.assertEqual(rep[0].num, 832)
        self.assertTrue(rep[5].text.endswith("10:15:18.68"))
        self.assertEqual(rep[5].text, '*** INFO [Task scheduler] 2020-11-18 10:15:18.68')

    def test_sup_regex(self):
        print("Test de sup_regex")
        self.AA.remove_carriage_return()
        self.AA.sup_regex(".*2020")
        self.AA.sup_regex('-----|Executing')
        self.assertEqual(len(self.AA), 857)

def test_suite():
    """Retourne la liste des tests à traiter."""
    tests = [unittest.makeSuite(CalculsTest)]
    return unittest.TestSuite(tests)


if __name__ == '__main__':
    """Programme de test de vérification."""
    # lancer les unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(CalculsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)