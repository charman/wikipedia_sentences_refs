#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import argparse
import json
import re
import sys
import urllib
import wiki2plain
import lxml.etree
import nltk  # for now.
from bs4 import BeautifulSoup
from string_scanner.scanner import Scanner
import mwparserfromhell
import sanitize_html


ENGLISH_LANG = 'en'

REFTOKEN_RE = re.compile(
    'coeref\d+',
    re.MULTILINE | re.DOTALL
)

def _handle_args(argv):
    """
    Use argparse module to handle command line arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l', '--language',
        default=ENGLISH_LANG,
        help='the language of the Wikipedia site.\n'
             'Choices include en, es, etc.'
    )
    parser.add_argument(
        'english_title',
        help='the title of the page on the English Wikipedia site to be '
             'processed'
    )
    parser.add_argument(
        '--quoted',
        action='store_true',
        help='the title of the Wikipedia page already has special characters '
             'replaced with the %%xx escape'
    )
    return parser.parse_args(argv[1:])

def scrape_wikitext(title, lang=ENGLISH_LANG):
    params = {
        "format":"xml",
        "action":"query",
        "prop":"revisions",
        "rvprop":"content",
        "rvlimit":"1",
        "redirects":"",
    }
    params["titles"] = "%s" % urllib.quote(title.encode('utf8'))
    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    url = "http://%s.wikipedia.org/w/api.php?%s" % (lang, qs)
    try:
        tree = lxml.etree.parse(urllib.urlopen(url))
    except:
        sys.exit(
            "0ERROR: the '%s' page could not be loaded in the language '%s'." %
            (title, lang)
        )
    revs = tree.xpath('//rev')
    if not revs:
        sys.exit(
            "1ERROR: the '%s' page could not be loaded in the language '%s'." %
            (title, lang)
        )
    wikitext = revs[-1].text.replace('\t', ' ')

    # Remove everything starting with the '<references\s*/>' tag.
    return unicode(re.split(r'<references\s*/>', wikitext)[0])

def redirected_title(english_title):
    """
    Returns the title of the page where this title redirects to. If there is no
    redirection, return the same title.
    """
    url = (
        'http://en.wikipedia.org/w/api.php?'
        'format=xml&'
        'action=query&'
        'titles=%s&'
        'redirects'
        % urllib.quote(english_title.encode('utf8'))
    )
    response = urllib.urlopen(url).read()
    soup = BeautifulSoup(response)
    redirection = soup.find('r')
    if redirection:
        return redirection['to']
    else:
        return english_title

def translated_title(english_title, lang):
    """
    Returns the name of the page that is a translation into the specified lang,
    of the english_title page.
    """
    url = (
        'http://en.wikipedia.org/w/api.php?'
        'format=xml&'
        'action=query&'
        'titles=%s&'
        'prop=langlinks&'
        'lllimit=500'
        % urllib.quote(english_title.encode('utf8'))
    )
    lang_links = urllib.urlopen(url).read()
    soup = BeautifulSoup(lang_links)
    try:
        return soup.find('ll', lang=lang).text
    except AttributeError:
        error_msg = (
            "ERROR: the '%s' page does not exist in the language '%s'." %
            (english_title, lang)
        )
        sys.exit(error_msg)

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

def fixup_named_refs(wikitext):
    """
    Replace named ref tags with bad syntax like <ref name=something/> with
    better syntax, like <ref name="something" />.
    """
    named_openclose_reftag_re = re.compile(r'<\s*ref\s*name\s*=\s*([^\s]+)/>')
    repl = r'<ref name="\1" />'
    return named_openclose_reftag_re.sub(repl, wikitext)

def collect_refs(wikitext):
    """
    Finds all the citations within named and unnamed <ref></ref> and <ref />
    tags, returns a copy of the wikitext with the reftag spans replaced with
    identifier tokens of the form 'coerefN' (without quotes, N is a decimal
    number).

    Also returns a dict that is a mapping of ref indentifier tokens as
    keys and a list of associated URLs as the values.

    The return value is a tuple containing the dict followed by the wikitext.
    """
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
            matched_url = re.match(r'\s*url\s*=\s*(\S+)\s*', unicode(ut.get('url')))
            if matched_url:
                url = matched_url.groups(1)[0]
                #result.append(ut.get('url').split('=')[-1].strip())
                result.append(url)
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
            # The first word of the next sentence (if the next sentence is not
            # empty):
            try:
              tokens.append(sent_tokens[sent_number + 1][0])
            except IndexError:
              pass

        for token_idx, token in enumerate(tokens):
            token_re = re.compile(token)

            # Get all the text until this token is matched, but don't match
            # anything inside <ref.*></ref> tags.
            # Collect the urls in this range.

            if scanner.check_to(token_re) is None:
                sys.exit(
                    '\nEverything after "{}" is:\n{}'.format(
                        token_re.pattern,
                        scanner.rest()
                    )
                )

            next_chunk = scanner.scan_to(token_re)

            # Move the scanner ahead, and make an assertion.
            #assert scanner.scan(token_re) is not None
            scanner.scan(token_re)

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

        # Ignore everything beginning with the References or Notes section header.
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

def main(argv):
    args = _handle_args(argv)
    language = args.language

    # Make sure this is the non-url-quoted title string.
    if args.quoted:
        english_title = urllib.unquote(args.english_title)
    else:
        english_title = args.english_title
    english_title = unicode(english_title, encoding='utf8')

    # Get the redirected title if necessary.
    english_title = redirected_title(english_title)

    # Get the translated title if necessary.
    if language == ENGLISH_LANG:
        title = english_title
    else:
        title = translated_title(english_title, language)

    # Download the page in wikitext format.
    wikitext = scrape_wikitext(title, language)
    # Since the result will be tab-separated text, remove all tabs from the
    # source.
    wikitext = wikitext.replace('\t', ' ')
    wikitext = wikitext.replace('&nbsp;', ' ')
    wikitext = fixup_named_refs(wikitext)
    wikitext = sanitize_html.safe_html(wikitext)
    wikitext = '\n'.join(line.strip() for line in wikitext.split('\n') if line.strip())

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

    # Discard lines that are not interesting.
    sentences_and_refurls = prune_lines(
        [sentence] + urls
        for sentence, urls in zip(sentences, line_urls)
    )

    # Print a list of sentences, each with all its associated URLs separated
    # by tabs.
    result_string = '\n'.join(
        '\t'.join(result) for result in sentences_and_refurls
    )
    return result_string

if __name__ == '__main__':
    print(main(sys.argv).encode('utf8'))