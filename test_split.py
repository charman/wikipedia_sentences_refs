# -*- encoding: utf-8 -*-
import unittest
from split import FreelingSentenceSplitter

class TestSentenceSplitter(unittest.TestCase):

    def test_freeling_es(self):
        input_sent = '* un régimen de comunicaciones e inspecciones frente a cualquier obra que pueda afectar la calidad de las aguas (arts. 7 a 12);'.decode('utf-8')
        expect = [
            '* un régimen de comunicaciones e inspecciones frente a cualquier obra que pueda afectar la calidad de las aguas (arts. 7 a 12);'.decode('utf-8'),
        ]
        actual = FreelingSentenceSplitter('es').split(input_sent)
        self.assertEqual(expect, actual)
