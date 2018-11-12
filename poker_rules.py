from enum import Enum
from deck import Rank
from deck import Suit
from collections import defaultdict


class PokerHand(Enum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    TRIPS = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    QUADS = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9


def hand_strength(hand):
    freq = defaultdict(int)
    for card in hand:
        freq[card.rank] += 1
    sorted_values = sorted(freq.values())

    if all(v == 1 for v in sorted_values): # high card, straight, flush
        is_straight = straight(hand)
        is_flush = flush(hand)
        ranks = [c.rank for c in hand]

        if is_straight and is_flush:
            if Rank.TEN in ranks and Rank.ACE in ranks:
                return PokerHand.ROYAL_FLUSH
            return PokerHand.STRAIGHT_FLUSH

        if is_straight:
            return PokerHand.STRAIGHT

        if is_flush:
            return PokerHand.FLUSH

        return PokerHand.HIGH_CARD

    elif sorted_values == [1,4] or sorted_values == [4]:
        return PokerHand.QUADS
    elif sorted_values == [2,3]:
        return PokerHand.FULL_HOUSE
    elif sorted_values == [1, 1, 3] or sorted_values == [1, 3] or sorted_values == [3]:
        return PokerHand.TRIPS
    elif sorted_values == [1, 2, 2] or sorted_values == [2, 2]:
        return PokerHand.TWO_PAIR

    return PokerHand.PAIR

def flush(hand):
    return len(hand) == 5 and len(set(c.suit for c in hand)) == 1


def straight(hand):
    if len(hand) < 5:
        return False

    ordered = sorted(hand, key=lambda c: c.rank.value)
    smallest_card = ordered[0]
    biggest_card = ordered[-1]

    if biggest_card.rank == Rank.ACE:
        ranks = [c.rank for c in ordered]
        return ranks in [[Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.ACE],
                         [Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE]]
    else:
        return len(set(c.rank for c in hand)) == 5 \
               and biggest_card.rank.value - smallest_card.rank.value == 4

