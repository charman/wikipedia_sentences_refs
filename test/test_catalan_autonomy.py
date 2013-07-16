# -*- encoding: utf-8 -*-
import unittest
from wikimedia_article_sentences_refs import *


class Test1(unittest.TestCase):

    def setUp(self):
        fn = 'test/resources/2010_Catalan_autonomy_protest.es.orig-wikitext.log'
        with open(fn) as f:
            self.wikitext_es = f.read().decode('utf-8')

        fn = 'test/resources/2010_Catalan_autonomy_protest.en.orig-wikitext.log'
        with open(fn) as f:
            self.wikitext_en = f.read().decode('utf-8')

    def test_es(self):
        self.assertNotEqual('', self.wikitext_es)

    def test_en(self):
        self.assertNotEqual('', self.wikitext_en)

    def test_url_extraction(self):
        wikitext = self.wikitext_es
        map_reftoken_to_urls, __ = collect_refs(wikitext)
        expect = u"http://www.3cat24.cat/especial/211/altres/El-TC-dicta-sentencia-per-lEstatut"
        actual = map_reftoken_to_urls["coeref0000"][0]
        self.assertEqual(expect, actual)


class TestStripWikitext(unittest.TestCase):

    def test_internal_double_sq_brackets(self):
        wikitext = """[[Archivo:Lema de la manifestació.JPG|thumb|230px|[[Lema]] de la [[manifestación]].]]\nLa""".decode('utf-8')
        expect = u'La'
        actual = strip_wikitext_markup(wikitext)
        self.assertEqual(expect, actual)


class TestCleanWikitext(unittest.TestCase):

    def test_internal_double_sq_brackets(self):
        wikitext = """[[Archivo:Lema de la manifestació.JPG|thumb|230px|[[Lema]] de la [[manifestación]].]]\nLa""".decode('utf-8')
        expect = """[[Archivo:Lema de la manifestació.JPG|thumb|230px|[[Lema]] de la [[manifestación]].]]\nLa""".decode('utf-8')
        actual = clean_wikitext(wikitext)
        self.assertEqual(expect, actual)
