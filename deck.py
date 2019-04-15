from enum import Enum
from collections import namedtuple
import random

Card = namedtuple("Card", ["rank", "suit"])


class Suit(Enum):
    DIAMONDS = 0
    CLUBS = 1
    HEARTS = 2
    SPADES = 3


class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


str_to_rank = {
    'A': Rank.ACE,
    'K': Rank.KING,
    'Q': Rank.QUEEN,
    'J': Rank.JACK,
    'T': Rank.TEN,
    '9': Rank.NINE,
    '8': Rank.EIGHT,
    '7': Rank.SEVEN,
    '6': Rank.SIX,
    '5': Rank.FIVE,
    '4': Rank.FOUR,
    '3': Rank.THREE,
    '2': Rank.TWO,
}

str_to_suit = {
    'd': Suit.DIAMONDS,
    'c': Suit.CLUBS,
    'h': Suit.HEARTS,
    's': Suit.SPADES,
}


def parse_card(s):
    assert len(s) == 2
    rank, suit = s
    return Card(str_to_rank[rank], str_to_suit[suit])


def parse_cards(arr):
    return [parse_card(s) for s in arr]


def card_to_str(card):
    suit_to_str = {v:k for k,v in str_to_suit.items()}
    rank_to_str = {v:k for k,v in str_to_rank.items()}
    return "{}{}".format(rank_to_str[card.rank], suit_to_str[card.suit])


def cards_to_str(cards):
    return "".join([card_to_str(c) for c in cards])


class Deck:
    deck_of_cards = set()

    def __init__(self):
        for suit in Suit:
            for rank in Rank:
                self.deck_of_cards.add(Card(rank, suit))

    def remove_card(self, card):
        self.deck_of_cards.discard(card)

    def remove_cards(self, cards):
        self.deck_of_cards -= set(cards)

    def choose(self, k): # Note: choose doesn't actually remove cards
        return random.sample(self.deck_of_cards, k)
