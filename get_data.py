#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import wiki2plain
import lxml.etree
import urllib
import nltk  # for now.
import re
import sys
from bs4 import BeautifulSoup
from string_scanner.scanner import Scanner
import mwparserfromhell
import sanitize_html


REFTOKEN_RE = re.compile(
    'coeref\d+',
    re.MULTILINE | re.DOTALL
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
    try:
        tree = lxml.etree.parse(urllib.urlopen(url))
    except:
        sys.exit("ERROR: the %s page could not be loaded." % title)
    revs = tree.xpath('//rev')
    wikitext = revs[-1].text.replace('\t', ' ')

    # Remove everything starting with the '<references\s*/>' tag.
    return unicode(re.split(r'<references\s*/>', wikitext)[0])

def split_sentences(text):
    """
    Return a list of sentences split using splitta. The only whitespace should
    be single space characters.
    """

    # Can I use splitta instead of nltk here?
    sent_detector = nltk.data.load(
        'tokenizers/punkt/%s.pickle' % 'english'
    ).tokenize

    # Ignore blank lines.
    result = []
    lines = text.split('\n')

    for line in lines:
        result.extend(
            line for line in sent_detector(line)
            if line.strip()
        )

    return result

def collect_refs(wikitext):

    reftokens_count = 0
    map_refnames_to_reftokens = {}
    map_reftoken_to_urls = {}
    soup = BeautifulSoup(wikitext)
    refs = soup.find_all('ref')

    if not refs:
        return {}, wikitext

    for ref in refs:

        # Collect all the citations' urls inside the ref tag span.
        urls = extract_ref_urls_from_wikitext(unicode(ref.string))
        name = None
        if 'name' in ref.attrs:
            name = unicode(ref.attrs['name'])

        if not name and not urls:
            ref.replace_with(' ')
            continue

        # Create a new reftoken if necessary.
        if not name in map_refnames_to_reftokens.keys():
            reftoken = 'coeref%s' % reftokens_count
            reftokens_count += 1
            if name:
                map_refnames_to_reftokens[name] = reftoken
        else:
            reftoken = map_refnames_to_reftokens[name]


        prev_urls = map_reftoken_to_urls.get(reftoken, set())
        prev_urls.update(urls)
        map_reftoken_to_urls[reftoken] = prev_urls

        ref.replace_with(' %s ' % reftoken)

    map_reftoken_to_urls = {k: list(v) for k, v in map_reftoken_to_urls.items()}
    return map_reftoken_to_urls, unicode(soup.get_text())


def extract_ref_urls_from_wikitext(wikitext):
    """
    Parse the wikitext and get all the urls found in cite/Citation templates.
    """
    wikicode = mwparserfromhell.parse(wikitext)
    url_templates = wikicode.filter_templates(
        recursive=True,
        matches=r'[cC]it\w+'
    )
    result = []
    for ut in url_templates:
        if ut.has_param('url'):
            result.append(ut.get('url').split('=')[-1].strip())
    return list(set(result))

def urls_for_lines(sentences, map_reftoken_to_urls, plain_text_with_reftokens):
    """
    Creates a list of lists. Each inner list is the list of URLs corresponding
    to the referenced citations for each line in the ``sentences`` argument.
    """
    result = []

    # Build a list of lists of tokens by splitting each sentence by
    # non-alphabet into tokens. Skip the empty strings.
    sent_tokens = [
        [
            token  for token in re.split(r'[^a-zA-Z]+', sent) if token != ''
        ]
        for sent in sentences
    ]

    scanner = Scanner()
    scanner.string = plain_text_with_reftokens

    for sent_number in range(len(sent_tokens)):
        urls = set()

        # Scan through the plain text, matching the second token in the
        # sentence through the first token of the following sentence.
        # Assume there are no refs before the first word in the first sentence.
        tokens = sent_tokens[sent_number][1:]

        if sent_number < len(sent_tokens) - 1:
            # The first word of the next sentence:
            try:
              tokens.append(sent_tokens[sent_number + 1][0])
            except IndexError:
              pass

        for token_idx, token in enumerate(tokens):
            token_re = re.compile(token)

            # Get all the text until this token is matched, but don't match
            # anything inside <ref.*></ref> tags.
            # Collect the urls in this range.
            next_chunk = scanner.scan_to(token_re)
            assert next_chunk is not None

            # Move the scanner ahead, and make an assertion.
            assert scanner.scan(token_re) is not None

            if sent_number == len(sent_tokens) - 1:
                if token_idx == len(sent_tokens[sent_number]) - 1:
                    # Handle the remaining text after the final token:
                    next_chunk += scanner.rest()
                    assert next_chunk is not None

            # Collect the urls for this line of text.
            flattend_urls_list = [
                url
                for reftoken in REFTOKEN_RE.findall(next_chunk)
                for url in map_reftoken_to_urls[reftoken]
            ]
            urls.update(flattend_urls_list)

        result.append(list(urls))

    return result

def prune_lines(sentences_and_refurls):
    """
    Ignore blank lines
    Ignore everything beginning with the References section header.
    Ignore all other section header lines
    Ignore sentences with fewer than 2 tokens
    """
    result = []
    for item in sentences_and_refurls:

        sent = item[0].strip()

        # Ignore blank lines
        if sent == '':
            continue

        # Ignore everything beginning with the References section header.
        if sent.strip('=') == 'References':
            break

        # Ignore all other section header lines
        if sent[0] == '=' and sent[-1] == '=':
            continue

        # Ignore all other section header lines
        if len(sent.split()) < 2:
            continue

        result.append(item)

    return result

def strip_wikitext_markup(wikitext):
    return unicode(wiki2plain.Wiki2Plain(wikitext).text)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('usage: %s wikipedia_page_title' % sys.argv[0])
        sys.exit(2)
    title = sys.argv[1]

    # Download the page in wikitext format.
    wikitext = scrape_wikitext(title)

    # Since the result will be tab-separated text, remove all tabs from the
    # source.
    wikitext.replace('\t', ' ')
    wikitext = sanitize_html.safe_html(wikitext)

    # Render a text-only representation of the page and sentence-split it.
    sentences = split_sentences(strip_wikitext_markup(wikitext))

    # Scan through the wikitext, collecting a map of (named and unnamed) refs
    # to urls, while also replacing each ref span with a token like
    # coeref0 coeref1 etc. Then use wiki2plain again on this version.
    map_reftoken_to_urls, wikitext_with_reftokens = collect_refs(wikitext)

    # Use the split tokens to scan the plain text version that has inserted
    # coeref tokens, and associate ref citation urls with sentences.
    line_urls = urls_for_lines(
        sentences,
        map_reftoken_to_urls,
        strip_wikitext_markup(wikitext_with_reftokens)
    )

    sentences_and_refurls = prune_lines(
        [sentence] + urls
        for sentence, urls in zip(sentences, line_urls)
    )

    # Print a list of sentences, each with all its associated URLs separated
    # by tabs.
    result_string = '\n'.join(
        '\t'.join(result) for result in sentences_and_refurls
    )
    print(result_string.encode('utf8'))
