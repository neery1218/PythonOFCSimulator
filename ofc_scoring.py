from enum import Enum
from poker_rules import PokerHand
from poker_rules import hand_strength
from poker_rules import Rank


class Row(Enum):
    TOP = 0
    MIDDLE = 1
    BOTTOM = 2


bottom_to_royalties = {
    PokerHand.ROYAL_FLUSH: 25,
    PokerHand.STRAIGHT_FLUSH: 15,
    PokerHand.QUADS: 10,
    PokerHand.FULL_HOUSE: 6,
    PokerHand.FLUSH: 4,
    PokerHand.STRAIGHT: 2,
}

middle_to_royalties = {
    PokerHand.ROYAL_FLUSH: 50,
    PokerHand.STRAIGHT_FLUSH: 30,
    PokerHand.QUADS: 20,
    PokerHand.FULL_HOUSE: 12,
    PokerHand.FLUSH: 8,
    PokerHand.STRAIGHT: 4,
    PokerHand.TRIPS: 2,
}


def royalties(row, row_pos):
    if row_pos == Row.BOTTOM:
        return bottom_to_royalties.get(hand_strength(row), 0)
    elif row_pos == Row.MIDDLE:
        return middle_to_royalties.get(hand_strength(row), 0)
    elif row_pos == Row.TOP:  # top
        strength = hand_strength(row)
        if strength == PokerHand.TRIPS:
            return 8 + 7.5 + row[0].rank.value
        elif strength == PokerHand.PAIR:
            pair_rank = row[0].rank.value if row[0].rank == row[2].rank else row[1].rank.value
            if pair_rank in [12, 13, 14]:  # fantasy land bonus
                pair_rank += 7.5
            if pair_rank in [2, 3, 4, 5]:
                return 0
            else:
                return pair_rank - 5
        elif strength == PokerHand.HIGH_CARD:
            return 0
        else:
            raise Exception("unexpected hand strength in top row")
    else:
        raise Exception("invalid row pos")
