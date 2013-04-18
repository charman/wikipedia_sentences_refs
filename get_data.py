#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import lxml.etree
import urllib
import nltk
#import wikipydia
import re
from wpTextExtractor import wiki2sentences
from bs4 import BeautifulSoup

title = "Barack Obama"

def scrape_wikitext(title):
    params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
    params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    url = "http://en.wikipedia.org/w/api.php?%s" % qs
    tree = lxml.etree.parse(urllib.urlopen(url))
    revs = tree.xpath('//rev')
    return revs[-1].text.encode('utf8')


def remove_refs_with_no_url(wikitext):
    pass

def remove_refs_with_no_url(wikitext):
    return re.sub(
        r'<ref>[^<]*(?!url)</ref>',
        '',
        wikitext,
        re.MULTILINE | re.UNICODE,
        )

def replace_refs_with_url(wikitext):

    # def next_ref_num():
    #     ref_num = 0
    #     while True:
    #         yield ref_num
    #         ref_num += 1

    # return
    #     re.sub(
    #         r'<ref>[^<]*url\s*=\s*()[^<]*</ref>',
    #         ' coereftag ',
    #         wikitext,
    #         re.MULTILINE | re.UNICODE,
    #         ),
    #     )

    # FYI: Alternative implementation

    soup = BeautifulSoup(wikitext)
    refs = soup.find_all('ref')
    ref_urls = []
    for i,r in enumerate(refs):
        r.replace_with(' coeref%i ' % i)
        ref_urls.append('http://www.wildplaces.co.uk/descent/descent168.html')
    return soup.text, ref_urls

def split_sentences(wikitext):
    sent_detector = nltk.data.load('tokenizers/punkt/%s.pickle' % 'english').tokenize
    all_sentences = wiki2sentences(wikitext, sent_detector, True)[0]
    results = []
    for sentence in all_sentences:
        if sentence != 'References':
            results.append(sentence)
        else:
            break
    return results


if __name__ == '__main__':
    title = 'Aquamole Pot'

    # Step @: download page in wikitext format
    wikitext = scrape_wikitext(title)

    # Step @: Replace {{ref}} tags that have a url with a word like
    wikitext
    # Step @: Split into sentences (using nltk)
    sentences = split_sentences(wikitext)

    # coerefN where N is an integer numeral.
    ref_num = 0

    # Step @: Get the citations
    # - step through the raw wiki text matching each of the next instance of
    # the words from the sent_detector step, ignoring {{text}} and
    # <ref>no url</ref>, and capturing each <ref>no url</ref> and the sentence
    # number it belongs to.

    # NO: replace the citation/ref with a placeholder before doing sentence detection.
    # NO: - if follows a period, insert placeholder before period.

    # Step @: Pruned everything starting with "References"

    # ? prune sentences shorter than a threshold (to get rid of headers?

    # Step @: Decide which references go with which sentences
    # The first token of the new sentence creates the boundary.

    # Step @: 


    # If the first token of new line is coerefN, then it belongs to the
    # previous line.

# TODO:
# use something to run the {{}} code
