import unittest
from wikimedia_article_sentences_refs import *
from wikimedia_article_sentences_refs.lib import _reftokens_for_sentence


class TestTokenScannerClass(unittest.TestCase):

    def setUp(self):
        self.scanner = TokenScanner("foo bar biz bang".split())

    @staticmethod
    def assign_neg1(scanner):
        try:
            scanner.position = -1
        except ValueError as e:
            raise e

    @staticmethod
    def assign_3(scanner):
        try:
            scanner.position = 3
        except ValueError as e:
            raise e

    def test_init(self):
        self.assertEqual(0, self.scanner.position)

    def test_set_valid_position(self):
        self.scanner.position = 3
        self.assertEqual(3, self.scanner.position)

    def test_set_valid_position_inside_method(self):
        TestTokenScannerClass.assign_3(self.scanner)
        self.assertEqual(3, self.scanner.position)

    def test_set_invalid_position_too_large(self):
        scanner = TokenScanner("")
        self.assertRaises(ValueError, TestTokenScannerClass.assign_3, scanner)

    def test_set_invalid_position_neg_value(self):
        TestTokenScannerClass.assign_neg1(self.scanner)

    def test_rest(self):
        self.scanner.position = 3
        self.assertEqual(['bang'], self.scanner.rest())

class TestReftokensForSentence(unittest.TestCase):

    def setUp(self):
        self.scanner = TokenScanner(u'a coeref0000 c'.split())

    def test_1_sentence(self):
        sentences = ['a b c']
        expect = ['coeref0000']
        actual = _reftokens_for_sentence(0, sentences, self.scanner)
        self.assertEqual(expect, actual)

    def test_2_sentences(self):
        sentences = ['a b', 'c']
        expect = ['coeref0000']
        actual = _reftokens_for_sentence(0, sentences, self.scanner)
        self.assertEqual(expect, actual)


class TestReftokensForSentences(unittest.TestCase):

    def setUp(self):
        self.wikitext_with_refs = (
            u'a coeref0000 \n'
            u'b coeref0001 \n'
            u'c coeref0002 \n'
        )

    def test_1_sentence(self):
        sentences = ['a', 'b', 'c']
        expect = [
            ['coeref0000'],
            ['coeref0001'],
            ['coeref0002'],
        ]
        actual = reftokens_for_sentences(sentences, self.wikitext_with_refs)
        self.assertItemsEqual(expect, actual)

