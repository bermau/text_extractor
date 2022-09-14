import unittest
from unittest.mock import patch

import lib_logstudy
from lib_logstudy import display_lines

i_file = r"../data_in/demo_short.log"

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
        self.AA = lib_logstudy.TextManipulator(i_file, encoding='ANSI')

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
        mock_print.assert_called_with("Number of lines :  3503")

    def test_len(self):
        print("Test de len")
        self.assertEqual(len(self.AA.n_lines), 3503)

    def test_sequence_1(self):
        print("Test de seq 1")
        self.AA.remove_carriage_return()
        rep = self.AA.get_first_ocurence_with_contexte("Dossier 20141709", before=2, after=3)
        self.assertEqual(len(rep), 6)
        self.assertEqual(rep[0].num, 832)
        self.assertTrue(rep[5].text.endswith("10:15:18.68"))
        self.assertEqual(rep[5].text, '*** INFO [Task scheduler] 2020-11-18 10:15:18.68')

    def test_sup_regex(self):
        print("Test de remove_regex")
        self.AA.remove_carriage_return()
        self.AA.remove_regex(".*2020")
        self.AA.remove_regex('-----|Executing')
        self.assertEqual(len(self.AA), 857)

    def test_select_lines(self):
        print("Test de select()")
        self.AA.remove_carriage_return()
        self.AA.remove_regex(".*2020")
        self.AA.select_lines(10, 16)
        self.assertEqual(self.AA.n_lines[0].num, 10)
        self.assertEqual(self.AA.n_lines[-1].num, 16)
        self.AA.cat()


def test_suite():
    """Retourne la liste des tests à traiter."""
    tests = [unittest.makeSuite(CalculsTest)]
    return unittest.TestSuite(tests)


if __name__ == '__main__':
    """Programme de test de vérification."""
    # lancer les unittests
    suite = unittest.TestLoader().loadTestsFromTestCase(CalculsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)