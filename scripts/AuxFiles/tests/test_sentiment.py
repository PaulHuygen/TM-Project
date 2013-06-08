from itertools import imap

from nose.tools import assert_true

from xtas.plugins.sentiment import SentimentLexiconTagger
from xtas.plugins.tokenizer import Token


def test_lexicontagger():
    # use imap to test iterable input
    pos_text = imap(Token, "wat een goed idee".split())
    neg_text = map(Token, "wat een afzichtelijk gedrocht".split())

    tag = SentimentLexiconTagger()

    pos_tags = tag(pos_text)
    neg_tags = tag(neg_text)

    assert_true(all(p.get("sentiment", 0) >= n.get("sentiment")
                    for p, n in zip(pos_tags, neg_tags)))
    assert_true(all(p.get("sentiment-positive") >= n.get("sentiment-positive")
                    for p, n in zip(pos_tags, neg_tags)))
    assert_true(any(p.get("sentiment-negative") < n.get("sentiment-negative")
                    for p, n in zip(pos_tags, neg_tags)))
    assert_true(all(p.get("sentiment-negative") <= n.get("sentiment-negative")
                    for p, n in zip(pos_tags, neg_tags)))
