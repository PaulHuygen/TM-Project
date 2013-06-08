# Author: Lars Buitinck.
# Based on earlier code by Daan Odijk.

from collections import Sequence
import logging
import os.path

#from settings import XTAS_PLUGIN_DATA_ROOT


logger = logging.getLogger(__name__)


# Path listed in previous version; we now ship the lexicon with the code.
#_DEFAULT_LEXICON = os.path.join(XTAS_PLUGIN_DATA_ROOT,
#                                "/semanticizer/nlwiki-20111104-wikipediaminer/",
#                                "sentiment_lexicon_nl.txt")
_DEFAULT_LEXICON = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sentiment_lexicon_nl.txt')


class SentimentLexiconTagger(object):
    """Simple, context-free sentiment analysis.

    Annotates words with their sentiment according to a lexicon.

    Parameters
    ----------
    lexicon_path: string, optional
        Path to a lexicon file. By default, a Dutch lexicon file shipped with
        xTas will be used.
    """
    # TODO Describe the syntax and semantics of the lexicon file.

    def __init__(self, lexicon_path=None):
        if lexicon_path == None:
            lexicon_path = _DEFAULT_LEXICON
        with open(lexicon_path) as f:
            sentiment = {}
            for ln in f:
                if ln[0] == '#':
                    continue
                w, signs = ln.strip().split(None, 1)
                pos, neg = signs.count('+'), signs.count('-')
                if w in sentiment:
                    logger.info("duplicate word %r, keeping value %r" % (w, signs))
                sentiment[w] = (pos / 4., neg / 4.)

        self._word_sentiment = sentiment

    def __call__(self, tokens):
        """Annotate a sequence of tokens, destructively.

        Adds attributes "sentiment-positive", "sentiment-negative" and
        "sentiment" to each token, representing a degree of sentiment in either
        direction represented as a number in the range [0, 1] and an overall
        sentiment (positive - negative, range [-1, 1]). Note that a term may be
        both positive and negative at the same time (to be decided in context).
        """
        tokens = _tosequence(tokens)
        for tok in tokens:
            try:
                pos, neg = self._word_sentiment[tok.term]
                if pos > 0:
                    tok["sentiment-positive"] = pos
                if neg > 0:
                    tok["sentiment-negative"] = neg
                if pos > 0 or neg > 0:
                    tok["sentiment"] = pos - neg
            except KeyError:
                pass

        return tokens


def _tosequence(x):
    if not isinstance(x, Sequence):
        x = list(x)
    return x


if __name__ == "__main__":
    from itertools import chain
    import sys
    from xtas.plugins.tokenizer import NLTKTokenizer

    logging.basicConfig(level=logging.WARN)
    sla = SentimentLexiconAnalyzer()
    tokenize = NLTKTokenizer()

    for tok in sla(chain(*map(tokenize, sys.argv[1:]))):
        print("%-10s  %s" % (tok.term, tok.attr.get("sentiment", "neutral")))
