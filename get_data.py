#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import lxml.etree
import urllib
import nltk
#import wikipydia
import re
from wpTextExtractor import wiki2sentences

title = "Barack Obama"

def scrape_wikitext(title):
    params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
    params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    url = "http://en.wikipedia.org/w/api.php?%s" % qs
    tree = lxml.etree.parse(urllib.urlopen(url))
    revs = tree.xpath('//rev')
    return revs[-1].text.encode('utf8')


if __name__ == '__main__':
    title = 'Aquamole Pot'

    # Step @: download page in wikitext format
    wikitext = scrape_wikitext(title)
    print wikitext
    #wikitext = wikipydia.query_text_raw(title, 'en')['text']

    # Step @: Get the citations
    # replace the citation/ref with a placeholder before doing sentence detection.
    # - if follows a period, insert placeholder before period.
    ref = re.compile(r'<ref>.*</ref>', re.MULTILINE & re.DOTALL)

    # Step @: Pruned everything starting with "References"

    # Step @: Split into sentences (using nltk)
    sent_detector = nltk.data.load('tokenizers/punkt/%s.pickle' % 'english').tokenize
    for sent in wiki2sentences(wikitext,sent_detector,True)[0]:
        print(sent.encode('utf-8'))

    # ? prune sentences shorter than a threshold (to get rid of headers?

    # Step @: Decide which references go with which sentences
    # The first token of the new sentence creates the boundary.

    # Step @: 

