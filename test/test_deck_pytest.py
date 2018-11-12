from deck import Deck
from deck import Card
from deck import Rank
from deck import Suit


def test_deck_size_is_52():
    deck = Deck()
    assert len(deck.deck_of_cards) == 52
    assert len(set(deck.deck_of_cards)) == 52


def test_remove_cards():
    deck = Deck()
    deck.remove_cards([Card(Rank.ACE, Suit.DIAMONDS), Card(Rank.KING, Suit.DIAMONDS)])
    assert len(deck.deck_of_cards) == 50

