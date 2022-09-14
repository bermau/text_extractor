import unittest
from unittest.mock import patch

import lib_logstudy
from lib_logstudy import display_lines

i_file = r"data_in/demo_log_72_lines.log"

def greet(name):
    print('Hello ', name)

def new_line():
    print("*" * 30)


class CalculsTest(unittest.TestCase):
    """Cette classe contient les méthodes qui, si elles commencent par le mot
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
    def test_printinfo(self, mock_print):
        self.AA.print_info()
        mock_print.assert_called_with("Number of lines :  72")

    def test_get_all_begin_end_block(self):
        print("Test de get_all_begin_end_block : Selectionner les blocks Task start/ Executing task")
        self.AA.remove_carriage_return()
        self.AA.cat()
        new_line()

        select = self.AA.get_all_begin_end_block(init_pattern="Task start:",
                                                 end_pattern="Executing task",
                                                 mark_block=False)
        display_lines(select)
        new_line()
        self.assertEqual(len(select), 21)

    def test_select_all_begin_end_block(self):
        self.AA.remove_carriage_return()
        self.AA.select_all_begin_end_block(init_pattern="Task start:",
                                                 end_pattern="Executing task",
                                                 mark_block=False)
        self.AA.cat()
        self.assertEqual(len(self.AA), 21)





def test_suite():
    """Retourne la liste des tests à traiter."""
    tests = [unittest.makeSuite(CalculsTest)]
    return unittest.TestSuite(tests)


if __name__ == '__main__':
    """Programme de test de vérification."""
    # lancer les unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(CalculsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)