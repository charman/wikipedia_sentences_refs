import codecs
import os
import re
import sys
import urllib
import urllib2
import unicodedata
import wiki2plain
import lxml.etree
import nltk  # for now.
from bs4 import BeautifulSoup
import mwparserfromhell
import sanitize_html


ENGLISH_LANG = 'en'
REFTOKEN_RE = re.compile(r'coeref\d+')
GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')


class LineWithRefs(object):

    def __init__(self, sentence='', urls=None):
        self._sent = sentence
        if not urls:
            urls = []
        self._urls = list(urls)

    @property
    def sentence(self):
        return self._sent

    @property
    def urls(self):
        return self._urls

    def __unicode__(self):
        return u'\t'.join([self.sentence] + self.urls)

    def __repr__(self):
        result = super(LineWithRefs, self).__repr__()
        result = result[:-1]  # Remove final '>' character.
        return u'{}; {}; {}>'.format(
            result,
            'sentence: %s' % self.sentence,
            'urls: %s' % self.urls,
        )


def scrape_wikitext(title, lang=ENGLISH_LANG, expand_templates=False, revision_timestamp=False):
    params = {
        "format": "xml",
        "action": "query",
        "prop": "revisions",
        "rvprop": "content",
        "rvlimit": "1",
        "redirects": "",
    }
    if expand_templates:
        params['rvexpandtemplates'] = ''
    if revision_timestamp:
        # MediaWiki accepts several different formats of timestamps:
        #   http://www.mediawiki.org/wiki/API:Data_formats#Timestamps
        params['rvstart'] = revision_timestamp
    params["titles"] = "%s" % urllib.quote(title.encode('utf-8'))
    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    url = "http://%s.wikipedia.org/w/api.php?%s" % (lang, qs)

    req = urllib2.Request(url)
    req.add_header('Charset', 'utf-8')
    try:
        xml_doc = urllib2.urlopen(req)
    except:
        sys.exit(
            "0ERROR: the '%s' page could not be loaded in the language '%s'." %
            (title, lang)
        )

    try:
        tree = lxml.etree.parse(xml_doc)
    except:
        sys.exit(
            "ERROR: the retrieved XML could not be parsed for page '%s' "
            "in language %s.\n" %
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

def fix_paragraph_boundaries(wikitext):
    return re.sub('\n\n+', '\n\n', wikitext, flags=re.MULTILINE)

def clean_wikitext(wikitext):
    """
    Preserve the wikitext markup, but remove certain characters that we don't
    want during parsing.

    * Replace tab characters with a single space character.
    * Replace non-blocking space string representation with a single space
      character.
    * Strip initial and final whitespace on all lines
    * Fix the number of consecutive newline characters to 2
    * prep the file to be parsed by an html parser.
    """

    # Replace undesireable characters and strings.
    wikitext = wikitext.replace(u'\ufeff', '')
    wikitext = wikitext.replace('\t', ' ')
    wikitext = wikitext.replace('&nbsp;', ' ')
    wikitext = sanitize_html.safe_html(wikitext)

    # Strip whitespace from every line.
    wikitext = '\n'.join(
        line.strip() for line in wikitext.split('\n')
    )

    # Fix the number of consecutive newline characters to 2.
    wikitext = re.sub(
        r'\n\n+',
        r'\n\n',
        wikitext,
        flags=re.UNICODE | re.MULTILINE
    )

    wikitext = fixup_named_refs(wikitext)
    return wikitext

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
        % urllib.quote(english_title.encode('utf-8'))
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
        % urllib.quote(english_title.encode('utf-8'))
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

def split_sentences(text, lang=ENGLISH_LANG):
    """
    Return a list of sentences split using splitta. The only whitespace should
    be single space characters.
    """

    if lang == ENGLISH_LANG:
        language = 'english'
    elif lang == 'es':
        language = 'spanish'
    else:
        language = 'english'

    # Can I use splitta instead of nltk here?
    sent_detector = nltk.data.load(
        'tokenizers/punkt/%s.pickle' % language
    ).tokenize

    # Don't ignore blank lines.
    result = []
    for line in text.split('\n'):
        result.extend(sent_detector(line))
    return result

def truncate_lines_after_match(line_re, text):
    r"""
    Keep all the lines from the beginning until the first line that matches the
    regular expression passed in.
    >>> truncate_lines_after_match('^\s*=*\s*Refs\s*=*\s*$', 'a\nb\n2')
    'a\nb\n2'
    >>> truncate_lines_after_match('^\s*=*\s*Refs\s*=*\s*$', 'a\n = Refs = \n2')
    'a'
    >>> truncate_lines_after_match('^\s*=*\s*Refs\s*=*\s*$', 'a\n=Refs=\n2')
    'a'
    """
    result = []
    for line in text.split('\n'):
        if re.match(line_re, line):
            break
        result.append(line)
    return '\n'.join(result)

def fixup_named_refs(wikitext):
    """
    Replace named ref tags with bad syntax like <ref name=something/> with
    better syntax, like <ref name="something" />.
    >>> fixup_named_refs('.<ref name=pais/><ref name=mundo/><ref name=vilaweb>{')
    '.<ref name="pais" /><ref name="mundo" /><ref name=vilaweb>{'
    """
    named_openclose_reftag_re = re.compile(
        r'<\s*ref\s*name\s*=\s*([^\s]+)/>',
        flags=(re.MULTILINE | re.UNICODE)
    )

    repl = r'<ref name="\1" />'
    return named_openclose_reftag_re.sub(repl, wikitext)

def collect_refs(wikitext, cit_url_attibutes_only=False):
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

        #from nose.tools import set_trace; set_trace() ## TEMP

        name = None
        if 'name' in ref.attrs.keys():
            name = unicode(ref.attrs['name'])

        # Collect all the citations' urls inside the ref tag span.
        urls = extract_urls_from_ref(
            unicode(ref.string),
            cit_url_attibutes_only
        )

        if not urls:
            ref.replace_with(' ')
            continue

        # Create a new reftoken if necessary.
        need_new_reftoken = (
            name is None
            or
            name not in map_refnames_to_reftokens.keys()
        )

        if need_new_reftoken:
            reftoken = 'coeref{0:04d}'.format(reftokens_count)
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


def extract_urls_from_ref(wikitext, cit_url_attibutes_only=False):
    """
    Parse the wikitext and get all the urls found
    set cit_url_attibutes_only=True to only capture urls in cite/Citation
    templates.
    """
    if not cit_url_attibutes_only:
        return [
            # Urls are being returned with '|.*' following the url,
            # so strip that away.
            mgroups[0].split('|')[0]
            for mgroups in GRUBER_URLINTEXT_PAT.findall(wikitext)
        ]

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
                # Urls are being returned with '|.*' following the url,
                # so strip that away.
                url = url.split('|')[0]
                if url:
                    result.append(url)
    return list(set(result))


def _reftokens_for_sentence(sent_number, sentences, scanner):
    sentence_wikitext = []

    sentence = sentences[sent_number]

    # An empty sentence has no reftokens.
    if not sentence:
        return []

    # Build a list of lists of tokens by splitting each sentence by
    # non-alphabet into tokens. Skip the empty strings.
    tokens = [
        token for token in re.split(r'\W+', sentence, flags=re.UNICODE)
        if token
    ]

    if not tokens:
        return []

    # Collection of the text parts between tokens in the split sentences:

    ## Locate the first token within the line and move past it.
    token = tokens[0]
    try:
        token_start = scanner.index(token)
        if token_start == len(scanner) - 1:
            scanner.position = -1
            return []
        elif token_start < len(scanner) - 1:
            # Ignore all the wikitext in front of the first token of the
            # sentence.
            scanner.position = token_start + 1
    except:
        pass

    ## Get all the other reftokens within the line.
    for token in tokens[1:]:
        wikitext_start = scanner.position
        try:
            wikitext_end = scanner.index(token)
        except:
            # Couldn't find this token, so skip it.
            sys.stderr.write('Couldn\'t find the token "%s"\n' % token)
            continue

        sentence_wikitext.extend(scanner[wikitext_start:wikitext_end])

        # Move past that token.
        if wikitext_end < len(scanner) - 1:
            scanner.position = wikitext_end + 1

    # Scanner should now be at the end of the last token in the sentence.

    # Get all the reftokens at the end of the line and at the beginning of the
    # next line.

    # Find next non-blank line if there is one, and
    # add the first non-empty string token from that line.
    last_token = None
    for sent in sentences[sent_number + 1:]:
        tokens = [
            token for token in re.split(r'\W+', sent, flags=re.UNICODE)
            if token
        ]

        if tokens:
            last_token = tokens[0]
            break

    if last_token:
        # Get next chunk of wikitext
        wikitext_start = scanner.position
        try:
            wikitext_end = scanner.index(last_token)
            sentence_wikitext.extend(scanner[wikitext_start:wikitext_end])
        # Don't move scanner past the last_token.
        except:
            pass

    else:
        # Scan to end of wikitext, collecting reftokens
        sentence_wikitext.extend(scanner[scanner.position:])
        scanner.position = -1

    # Collect the reftokens
    reftokens = set()
    for reftoken in REFTOKEN_RE.findall(' '.join(sentence_wikitext)):
        reftokens.add(reftoken)

    return list(reftokens)


class TokenScanner(list):
    """
    A TokenScanner is meant to store a list of unicode objects.
    the position property can be used to store the current index as the object
    is used to scan through the list of tokens.
    """

    def __init__(self, content):
        self._position = 0
        return super(TokenScanner, self).__init__(content)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if value > len(self) - 1:
            raise ValueError(
                "position cannot be greater than the length of the string."
            )
        self._position = value

    def rest(self):
        """
        Returns a unicode object with the contents of the Scanner from the
        Scanner.position to the end.
        """
        return self[self.position:]


def urls_from_reftokens(reftokens, map_reftoken_to_urls):
    """
    Replace the reftokens with URLs.
    """
    urls = set()
    for reftoken in reftokens:
        for url in map_reftoken_to_urls[reftoken]:
            urls.add(url)

    return list(urls)


def reftokens_for_sentences(sentences, plain_text_with_reftokens):
    result = []
    wikitext_tokens = [
        token for token in re.split(
            r'\W+', plain_text_with_reftokens, flags=re.UNICODE
        )
        if token
    ]
    scanner = TokenScanner(wikitext_tokens)

    # Collect reftokens for each sentence.
    for sent_number in range(len(sentences)):

        reftokens = _reftokens_for_sentence(
            sent_number,
            sentences,
            scanner
        )
        result.append(reftokens)

        if scanner.position == -1:
            break

    return result


def prune_lines(sentences_and_refurls):
    """
    Don't ignore blank lines
    Ignore everything beginning with the References section header.
    Ignore all other section header lines
    Ignore sentences with fewer than 2 tokens
    """
    result = []
    for item in sentences_and_refurls:

        sent = item[0].strip()

        # Ignore blank lines
        if sent != '':
            # Ignore everything beginning with the References or Notes section
            # header.
            if sent.strip('=') == 'References':
                break

            # # Ignore all other section header lines
            # if sent[0] == '=' and sent[-1] == '=':
            #     continue

            # # Ignore all other section header lines
            # if len(sent.split()) < 2:
            #     continue

        result.append(item)

    return result

def strip_wikitext_markup(wikitext):
    """
    Strip away markup elements:
    """

    # Strip ==Section Heading== markup
    wikitext = '\n'.join(
        line.strip().strip('=').strip() for line in wikitext.split('\n')
    )

    # # Strip [[File: ]] and similar markup.
    # wikitext = re.sub(
    #     r'\[\[(File|Archivo):.*?\]\]',
    #     r'',
    #     wikitext,
    #     flags=re.UNICODE | re.MULTILINE
    # )

    # Strip other markup
    body = BeautifulSoup(wikitext).body
    for table in body.find_all('table'):
        table.extract()
    for ref in body.find_all('ref'):
        ref.replace_with(' ')
    return wiki2plain.Wiki2Plain(unicode(body.text)).text

def write_log_file(logdir, filename, text):
    filename = unicode(filename)
    filename = unicodedata.normalize('NFKD', filename).encode('ascii','ignore')
    filename = re.sub(r'["\'?\s]', '_', filename)
    if logdir:
        with codecs.open(os.path.join(logdir, filename), 'w', 'utf-8') as f:
            f.write(text)

