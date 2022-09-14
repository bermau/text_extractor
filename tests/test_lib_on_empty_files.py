import unittest
from unittest.mock import patch

import lib_logstudy
from lib_logstudy import display_lines

i_file = r"../data_in/demo_log_10_lines_with_empty_lines.log"

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

    def test_remove_empty_lines(self):
        print("remove_empty_lines : intial fil contains 11 lines with 2 empty lines")
        self.AA.remove_carriage_return()
        self.AA.cat()
        new_line()
        self.AA.remove_empty_lines()
        self.AA.cat()
        self.assertEqual(len(self.AA), 9)


def test_suite():
    """Retourne la liste des tests à traiter."""
    tests = [unittest.makeSuite(CalculsTest)]
    return unittest.TestSuite(tests)


if __name__ == '__main__':
    """Programme de test de vérification."""
    # lancer les unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(CalculsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)