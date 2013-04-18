#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import lxml.etree
import urllib
import nltk  # for now.
import re
from wpTextExtractor import wiki2sentences
from bs4 import BeautifulSoup
from string_scanner.scanner import Scanner
import mwparserfromhell

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
    """
    Return a list of sentences split using splitta. The only whitespace should
    be single space characters.
    """
    # Can I use splitta instead of nltk here?
    sent_detector = nltk.data.load(
            'tokenizers/punkt/%s.pickle' % 'english'
        ).tokenize
    all_sentences = wiki2sentences(wikitext, sent_detector, True)[0]

    # Only return sentences that occur above a "References" line.
    results = []
    for sentence in all_sentences:
        if sentence != 'References':
            results.append(sentence)
        else:
            break
    return results

def extract_ref_urls_from_wikitext(wikitext):
    wikicode = mwparserfromhell.parse(wikitext)
    url_templates = wikicode.filter_templates(
            recursive=True,
            matches=r'{cite|Citation}.*'
        )
    result = []
    for ut in url_templates:
        if ut.has_param('url'):
            result.append(ut.get('url').split('=')[-1].strip())
    return result


if __name__ == '__main__':
    #title = 'Aquamole Pot'
    title = 'Barack Obama'

    # download page in wikitext format
    wikitext = scrape_wikitext(title)

    # Delete everthing from the first `<references\s*/>' tag to the end.

    # Render as plain text without tags and templates
    # Split into sentences, Save the sentences.
    sentences = split_sentences(wikitext)

    # Build a list of lists of tokens by splitting each sentence by
    # non-alphabet into tokens.
    sent_tokens = [re.split(r'[^a-zA-Z]+', sent) for sent in sentences]

    # For each sentence-level list, scan the original wikitext for each token,
    # collecting the citations that have URLs, saving the URLs and the sentence
    # number that they belong to.
    scanner = Scanner()
    scanner.string = wikitext
    result = []
    for sent_number in range(len(sent_tokens)):
        urls = set()
        # Assume there are no refs before the first word in the sentence.
        tokens = sent_tokens[sent_number][1:]
        if sent_number < len(sent_tokens) - 1:
            # The first word of the next sentence:
            tokens.append(sent_tokens[sent_number + 1][0])
        for token in tokens:
            # Get all the text until this token is matched.
            token_re = re.compile(token)
            wikitext_chunk = scanner.scan_to(token_re)
            # Collect the urls in this range.
            urls.update(extract_ref_urls_from_wikitext(wikitext_chunk))
            # Scan just past this token.
        if sent_number == len(sent_tokens) - 1:
            urls.update(extract_ref_urls_from_wikitext(scanner.rest()))
        # Save a list with the sentence text followed by each of the found
        # reference urls.
        result.append([sentences[sent_number]] + list(urls))

    # ? prune sentences shorter than a threshold (to get rid of headers?

    # Return a list of sentences, each with all its associated URLs separated
    # by tabs.
    with open('result.tsv', 'w') as fh:
        for sentence_and_urls in result:
            line = '\t'.join(sentence_and_urls)
            fh.write(line.encode('utf8') + '\n')
