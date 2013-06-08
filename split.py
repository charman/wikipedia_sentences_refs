# -*- encoding: utf-8 -*-
import sys
from subprocess import Popen, PIPE
import nltk  # for now.
import splitta_tokenizer

class SentenceSplitter(object):
    def __init__(self, lang_code):
        self._lang = lang_code

    @property
    def language(self):
        return self._lang

    def split(self):
        pass


class SplittaSentenceSplitter(SentenceSplitter):

    def split(self, input_text):
        return splitta_tokenizer.tokenize(input_text, model_path='model_svm')


class FreelingSentenceSplitter(SentenceSplitter):

    def split(self, input_text):
        cmd = ['/home/hltcoe/mmitchell/SCALE/spanish_sentence_split.sh']
        p = Popen(cmd, stdin=PIPE, stderr=PIPE, stdout=PIPE)
        out, err = p.communicate(input_text.encode('utf-8'))
        #if not p.returncode:
        #    sys.stderr.write(err.decode('utf-8'))
        #    raise IOError
        return out.decode('utf-8').strip('\n').split('\n')


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


if __name__ == '__main__':
    FreelingSentenceSplitter('es').split('hi')
