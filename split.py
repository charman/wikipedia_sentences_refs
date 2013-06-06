# -*- encoding: utf-8 -*-
import nltk  # for now.

class SentenceSplitter(object):
    def __init__(self, lang_code):
        self._lang = lang_code

    @property
    def language(self):
        return self._lang



class FreelingSentenceSplitter(SentenceSplitter):

    def split(self, input_text):
        return [
            '* un régimen de comunicaciones e inspecciones frente a cualquier '
            'obra que pueda afectar la calidad de las aguas '
            '(arts. 7 a 12);'.decode('utf-8')
        ]


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
    return text.split('\n')


def new_splitter(lang):
    lang_splitter = {
        'en': SplittaSentenceSplitter,
        'es': FreelingSentenceSplitter,
    }
    return lang_splitter[lang](lang)
