# -*- encoding: utf-8 -*-
import unittest
import get_sents_refs


class Test1(unittest.TestCase):

    def setUp(self):
        fn = 'resources/2010_Catalan_autonomy_protest.es.orig-wikitext.log'
        with open(fn) as f:
            self.wikitext_es = f.read().decode('utf-8')

        fn = 'resources/2010_Catalan_autonomy_protest.en.orig-wikitext.log'
        with open(fn) as f:
            self.wikitext_en = f.read().decode('utf-8')

    def test_es(self):
        self.assertNotEqual('', self.wikitext_es)

    def test_en(self):
        self.assertNotEqual('', self.wikitext_en)


class TestStripWikitext(unittest.TestCase):

    def test_internal_double_sq_brackets(self):
        wikitext = """[[Archivo:Lema de la manifestació.JPG|thumb|230px|[[Lema]] de la [[manifestación]].]]\nLa""".decode('utf-8')
        expect = u'La'
        actual = get_sents_refs.strip_wikitext_markup(wikitext)
        self.assertEqual(expect, actual)


class TestCleanWikitext(unittest.TestCase):

    def test_internal_double_sq_brackets(self):
        wikitext = """[[Archivo:Lema de la manifestació.JPG|thumb|230px|[[Lema]] de la [[manifestación]].]]\nLa""".decode('utf-8')
        expect = """[[Archivo:Lema de la manifestació.JPG|thumb|230px|[[Lema]] de la [[manifestación]].]]\nLa""".decode('utf-8')
        actual = get_sents_refs.clean_wikitext(wikitext)
        self.assertEqual(expect, actual)
