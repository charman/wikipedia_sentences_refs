import unittest
from wikimedia_article_sentences_refs import *

CATALAN_DIR = 'test/resources/catalan'
log_filenames = (
    '2010_Catalan_autonomy_protest.clean-wikitext.log',
    '2010_Catalan_autonomy_protest.map_reftoken_to_urls.log',
    '2010_Catalan_autonomy_protest.orig-wikitext.log',
    '2010_Catalan_autonomy_protest.sentences.log',
    '2010_Catalan_autonomy_protest.urls.log',
    '2010_Catalan_autonomy_protest.wikitext_with_reftokens.log',
)

log_paths = (
    "{0}/{1}".format(CATALAN_DIR, fn)
    for fn in log_filenames
)


with open(log_paths.next()) as f:
    text = f.read().decode('utf-8')
    catln_clean_wikitext = text

with open(log_paths.next()) as f:
    text = f.read()
    catln_map_reftoken_to_urls = eval(text)

with open(log_paths.next()) as f:
    text = f.read().decode('utf-8')
    catln_wikitext = text

with open(log_paths.next()) as f:
    text = f.read().decode('utf-8')
    catln_sentences = text.split('\n')

with open(log_paths.next()) as f:
    text = f.read().decode('utf-8')
    catln_urls = [
        urls.split('\t')
        for urls in text.split('\n')
    ]

with open(log_paths.next()) as f:
    text = f.read().decode('utf-8')
    catln_wikitext_with_reftokens = text


class TestCatalan(unittest.TestCase):

    def test_clean_wikitext(self):
        expect = catln_clean_wikitext
        actual = clean_wikitext(catln_wikitext)
        self.assertItemsEqual(expect, actual)

    def test_map_reftoken_to_urls__map(self):
        expect = catln_map_reftoken_to_urls
        actual, __ = collect_refs(catln_clean_wikitext)
        self.assertItemsEqual(expect, actual)

    def test_map_reftoken_to_urls__map(self):
        expect = catln_wikitext_with_reftokens
        __, actual = collect_refs(catln_clean_wikitext)
        self.assertEqual(
            expect,
            actual,
            u"\n***expect:***\n{0}\n***actual:***\n{1}\n".format(
                expect, actual
            ).encode('utf-8')
        )
