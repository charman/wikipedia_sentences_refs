# -*- encoding: utf-8 -*-
import unittest
import get_sents_refs


class Test1(unittest.TestCase):

    def setUp(self):
        fn = 'resources/Manifestacion__Som_una_nacio._Nosaltres_decidim_.orig-wikitext.log'
        with open(fn) as f:
            self.wikitext = f.read().decode('utf-8')

    def test_1(self):
        self.assertNotEqual('', self.wikitext)


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
