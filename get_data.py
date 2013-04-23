#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import lxml.etree
import urllib
import nltk  # for now.
import re
import sys
from wpTextExtractor import wiki2sentences
from bs4 import BeautifulSoup
from string_scanner.scanner import Scanner
import mwparserfromhell

REFTAG_OPEN_RE = re.compile(
    r'<ref.*?>',
    re.MULTILINE | re.DOTALL | re.IGNORECASE
)
REFTAG_NAMED_OPEN_RE = re.compile(
    r'<ref.*?name\s*=\s*[\'\"](?P<name>\S+[\'\"]).*?[^\/]>',
    re.MULTILINE | re.DOTALL | re.IGNORECASE
)
REFTAG_CLOSE_RE = re.compile(
    r'</ref>',
    re.MULTILINE | re.DOTALL | re.IGNORECASE
)
REFTAG_NAMED_COMBINED_RE = re.compile(
    r'<ref.*?name\s*=\s*[\'\"](?P<name>\S+[\'\"]).*?>',
    re.MULTILINE | re.DOTALL | re.IGNORECASE
)
TEMPLATE_OPEN_RE = re.compile(
    r'{{',
    re.MULTILINE | re.DOTALL | re.IGNORECASE
)
TEMPLATE_CLOSE_RE = re.compile(
    r'}}',
    re.MULTILINE | re.DOTALL | re.IGNORECASE
)

def scrape_wikitext(title):
    params = {
        "format":"xml",
        "action":"query",
        "prop":"revisions",
        "rvprop":"timestamp|user|comment|content"
    }
    params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    url = "http://en.wikipedia.org/w/api.php?%s" % qs
    tree = lxml.etree.parse(urllib.urlopen(url))
    revs = tree.xpath('//rev')
    wikitext = revs[-1].text.replace('\t', ' ')
    # remove everything starting with the '<references\s*/>' tag.
    return re.split(r'<references\s*/>', wikitext)[0]

def split_sentences(wikitext):
    """
    Return a list of sentences split using splitta. The only whitespace should
    be single space characters.
    """
    # Can I use splitta instead of nltk here?
    sent_detector = nltk.data.load(
            'tokenizers/punkt/%s.pickle' % 'english'
        ).tokenize
    return wiki2sentences(wikitext, sent_detector, True)[0]

def extract_ref_urls_from_wikitext(wikitext):
    wikicode = mwparserfromhell.parse(wikitext)
    url_templates = wikicode.filter_templates(
        recursive=True,
        matches=r'[cC]it\w+'
    )
    result = []
    for ut in url_templates:
        if ut.has_param('url'):
            result.append(ut.get('url').split('=')[-1].strip())
    return result

def _get_next_wikitext_chunk(scanner, token):
    #token_re = re.compile(token, re.MULTILINE | re.DOTALL)
    token_re = re.compile(token)
    num_reftag_open = 0
    num_reftag_close = -1
    num_template_open = 0
    num_template_close = -1
    wikitext_chunk = ''
    while num_reftag_open > num_reftag_close or \
            num_template_open > num_template_close:
        # If this is not the first time through the loop, the token was found
        # inside a pair of <ref></ref> tags.
        if num_reftag_close == -1:
            num_reftag_close = 0
        if num_template_close == -1:
            num_template_close = 0
        #sys.stderr.write(scanner.check_until(token))
        next_chunk = scanner.scan_to(token_re)
        scanner.scan(token_re)
        if next_chunk:
            num_reftag_open += len(REFTAG_OPEN_RE.findall(next_chunk))
            num_reftag_close += len(REFTAG_CLOSE_RE.findall(next_chunk))
            num_template_open += len(TEMPLATE_OPEN_RE.findall(next_chunk))
            num_template_close += len(TEMPLATE_CLOSE_RE.findall(next_chunk))
            wikitext_chunk = ''.join([wikitext_chunk, next_chunk, token])
        #sys.stderr.write(wikitext_chunk)
    return wikitext_chunk

def get_ref_names_citations(wikitext):
    """
    Parse the <ref name="X"></ref> and <ref name = 'X' /> tags and build a
    mapping of ref tag name to all its associated citation urls.

    Return an empty dict if none is found.
    """
    soup = BeautifulSoup(wikitext)
    result = {}
    refs = soup.find_all('ref')
    if not refs:
        return {}
    for ref in [ref for ref in refs if 'name' in ref.attrs]:
        name = ref.attrs['name']
        urls = extract_ref_urls_from_wikitext(unicode(ref.string))
        if urls:
            new_urls = result.get(name, set())
            new_urls.update(urls)
            result[name] = new_urls
    if not result.items():
        return {}
    return {k: list(v) for k,v in result.items()}

def collect_citations(sentences, wikitext):
    """
    Build a list of lists of tokens by splitting each sentence by non-alphabet
    into tokens.
    """
    ref_names_citations = {}
    # Parse the wikitext on a first pass:
    # Extract all the named refs and the citations with URLs found within.

    # Pass through the sentences, Find the name of the ref for each

    sent_tokens = [re.split(r'[^a-zA-Z]+', sent) for sent in sentences]
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
            # Get all the text until this token is matched, but don't match
            # anything inside <ref.*></ref> tags.
            # Collect the urls in this range.
            urls.update(extract_ref_urls_from_wikitext(_get_next_wikitext_chunk(
                scanner, token
            )))
            #print token.encode('utf8')
        if sent_number == len(sent_tokens) - 1:
            urls.update(extract_ref_urls_from_wikitext(scanner.rest()))
        # Save a list with the sentence text followed by each of the found
        # reference urls.
        result.append(list(urls))
    return result

if __name__ == '__main__':
    #title = 'Aquamole Pot'
    #title = 'Barack Obama'
    if len(sys.argv) != 2:
        print('usage: %s wikipedia_page_title' % sys.argv[0])
        sys.exit(2)
    title = sys.argv[1]

    # download page in wikitext format
    wikicode = mwparserfromhell.parse(scrape_wikitext(title))
    for node in wikicode.nodes:
        try:
            name = node.name.__unicode__()
            if not re.match(r'\s*[Cc]it.*', name) \
                    and not re.match(r'\s*Reflist.*', name):
                wikicode.remove(node)
        except AttributeError:
            pass
    wikitext = wikicode.__unicode__()

    # Render as plain text without tags and templates
    # Split into sentences, Save the sentences.
    sentences = split_sentences(wikitext)

    # For each sentence-level list, scan the original wikitext for each token,
    # collecting the citations that have URLs, saving the URLs and the sentence
    # number that they belong to.
    result = zip(sentences, collect_citations(sentences, wikitext))

    # ? prune sentences shorter than a threshold (to get rid of headers?

    # Print a list of sentences, each with all its associated URLs separated
    # by tabs.
    print(
        '\n'.join('\t'.join([sentence] + urls) for sentence, urls in result)
    ).encode('utf8')
