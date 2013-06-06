# -*- encoding: utf-8 -*-
import unittest
from split import FreelingSentenceSplitter, new_splitter

class TestSentenceSplitter(unittest.TestCase):

    def setUp(self):
        self.input_sent1 = (
            '* un régimen de comunicaciones e inspecciones frente a cualquier '
            'obra que pueda afectar la calidad de las aguas '
            '(arts. 7 a 12);\n'.decode('utf-8')
        )
        self.input_sent2 = 'Hola, mundo. ¿Cómo están?\n'.decode('utf-8')
        self.expected_output1 = [
            '* un régimen de comunicaciones e inspecciones frente a cualquier obra que pueda afectar la calidad de las aguas (arts. 7 a 12);'.decode('utf-8'),
        ]
        self.expected_output2 = [
            u'Hola, mundo.',
            '¿Cómo están?'.decode('utf-8')
        ]

    def test_freeling_es1(self):
        input_sent = self.input_sent1
        expect = self.expected_output1
        actual = FreelingSentenceSplitter('es').split(input_sent)
        self.assertEqual(expect, actual)

    def test_freeling_es2(self):
        input_sent = self.input_sent2
        expect = self.expected_output2
        actual = FreelingSentenceSplitter('es').split(input_sent)
        self.assertEqual(expect, actual)

    def test_new_splitter_es1(self):
        splitter = new_splitter('es')
        expect = self.expected_output1
        actual = splitter.split(self.input_sent1)
        self.assertEqual(expect, actual)

    def test_new_splitter_es2(self):
        splitter = new_splitter('es')
        expect = self.expected_output2
        actual = splitter.split(self.input_sent2)
        self.assertEqual(expect, actual)
