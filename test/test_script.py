import unittest
from subprocess import Popen, PIPE

SCRIPT_PATH = './scripts/get_sentences_and_refs'

class TestSpanish(unittest.TestCase):

    def test_english_Aquamole_Pot(self):
        cli_argv = [SCRIPT_PATH, '-l', 'en', 'Aquamole Pot']
        p = Popen(cli_argv, stdout=PIPE)
        result = len(p.communicate())
        self.assertTrue(result > 0)

