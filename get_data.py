#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import lxml.etree
import urllib
import nltk  # for now.
import re
import sys
from wpTextExtractor import wiki2sentences
from bs4 import BeautifulSoup, Comment
from string_scanner.scanner import Scanner
import mwparserfromhell
import sanitize_html

TAG_OPEN_RE = re.compile(
    r'<(?!--)[^\/].*?[^\/]>',
    re.MULTILINE | re.DOTALL
)
TAG_CLOSE_RE = re.compile(
    r'<\/.*?[^\/]>',
    re.MULTILINE | re.DOTALL
)
TAG_OPENCLOSE_RE = re.compile(
    r'<[^\/].*?\/>|<!--.*?-->',
    re.MULTILINE | re.DOTALL
)
TEMPLATE_OPEN_RE = re.compile(
    r'{{',
    re.MULTILINE | re.DOTALL
)
TEMPLATE_CLOSE_RE = re.compile(
    r'}}',
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
    sentences = wiki2sentences(wikitext, sent_detector, True)[0]
    result = []
    for sent in sentences:
        if sent.strip() == 'References':
            break
        result.append(sent)
    return result


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
    return sorted(list(set(result)))

def _inside_openclose_tag(wikitext):
    """
    This basically answers whether the final '<' character is to the right of
    the final '>' character, indicating that the wikitext at the end is inside
    a tag.
    """
    return wikitext.rfind('<') > wikitext.rfind('>')

def _get_next_wikitext_chunk(scanner, token):
    """
    Return all the wikitext from the scanner's position when entering this
    method until (and including) the token. Care is taken to ignore any matches
    inside ref tags.
    """
    token_re = re.compile(token)
    num_tag_open, num_tag_close = 0, 0
    num_template_open, num_template_close = 0, 0
    wikitext_chunk = ''
    keep_scanning = True

    while keep_scanning:

        next_chunk = scanner.scan_to(token_re)
        #print(next_chunk.encode('utf8'))  # TEMP
        #print(token.encode('utf8'))  # TEMP
        assert next_chunk is not None
        assert scanner.scan(token_re) is not None
        if next_chunk:
            num_tag_open += len(TAG_OPEN_RE.findall(next_chunk))
            num_tag_close += len(TAG_CLOSE_RE.findall(next_chunk))
            num_template_open += len(TEMPLATE_OPEN_RE.findall(next_chunk))
            num_template_close += len(TEMPLATE_CLOSE_RE.findall(next_chunk))
            wikitext_chunk = ' '.join([wikitext_chunk, next_chunk, token])
        #else:
        #    print('****')
        #    print(next_chunk.encode('utf8'))
        #    print('****')
        #    sys.exit(2)

        inside_a_tag_span = num_tag_open > num_tag_close or \
            _inside_openclose_tag(wikitext_chunk)
        inside_a_template_span = num_template_open > num_template_close
        if not (inside_a_tag_span or inside_a_template_span):
            keep_scanning = False

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
        name = unicode(ref.attrs['name'])
        urls = extract_ref_urls_from_wikitext(unicode(ref.string))
        if urls:
            new_urls = result.get(name, set())
            new_urls.update(urls)
            result[name] = new_urls
        else:
            result[name] = set()
    if not result.items():
        return {}
    result = {k: list(v) for k,v in result.items()}
    #for k in result.keys():
    #    print(k.encode('utf8'))
    #sys.exit()
    #return result

def _replace_named_refs_with_urls(wikitext, ref_urls_map):
    soup = BeautifulSoup(wikitext)
    result = set()
    refs = soup.find_all('ref')
    if refs:
        for ref in [ref for ref in refs if 'name' in ref.attrs]:
            name = unicode(ref.attrs['name'])
            result.update(ref_urls_map[name])
    return result

def collect_citations(sentences, wikitext):
    """
    Build a list of lists of tokens by splitting each sentence by non-alphabet
    into tokens.
    """
    # Parse the wikitext on a first pass,
    # Extract all the named refs and the citations with URLs found within:
    ref_names_citations = get_ref_names_citations(wikitext)

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
            next_chunk = _get_next_wikitext_chunk(scanner, token)
            urls.update(extract_ref_urls_from_wikitext(next_chunk))
            urls.update(
                _replace_named_refs_with_urls(next_chunk, ref_names_citations)
            )
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

    # Download the page in wikitext format.
    wikicode = mwparserfromhell.parse(scrape_wikitext(title))
    for node in wikicode.nodes:
        try:
            name = node.name.__unicode__()
            if not re.match(r'\s*[Cc]it.*', name) \
                    and not re.match(r'\s*Reflist.*', name):
                wikicode.remove(node)
        except AttributeError:
            pass
        if isinstance(node, mwparserfromhell.nodes.Wikilink):
            before = unicode(node)
            replacement_text = node.text or node.title
            replacement_node = mwparserfromhell.nodes.Text(unicode(replacement_text))
            after = unicode(replacement_node)
            wikicode.replace(node, replacement_node)
            #print("before: {}".format(before).encode('utf8'))  # TEMP
            #print("after: {}".format(after).encode('utf8'))  # TEMP

    wikitext = sanitize_html.safe_html(unicode(wikicode))
    #print(wikitext.encode('utf8'))  # TEMP

    # Render as plain text without tags and templates
    # Split into sentences, Save the sentences.
    sentences = split_sentences(wikitext)

    #print('\n'.join(sentences).encode('utf8'))  # TEMP
    #sys.exit()

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
