from poker_rules import hand_strength
from ofc_scoring import royalties
from ofc_scoring import Row
from poker_rules import PokerHand
from collections import defaultdict
from deck import cards_to_str


class OfcRow:
    def __init__(self, num_cards, cards=None):
        self.num_cards = num_cards
        self.row = [c for c in cards] if cards else []

    @property
    def completed(self):
        return len(self.row) == self.num_cards

    @property
    def total_cards(self):
        return len(self.row)

    def add_card(self, card):
        assert len(self.row) + 1 <= self.num_cards
        self.row.append(card)

    def __eq__(self, other):
        other_strength = hand_strength(other.row)
        self_strength = hand_strength(self.row)

        if self_strength.value != other_strength.value:
            return False
        else:
            self_ranks = sorted([c.rank.value for c in self.row])
            other_ranks = sorted([c.rank.value for c in other.row])
            return self_ranks == other_ranks

    def __le__(self, other):
        return self == other or self < other

    def __lt__(self, other):
        other_strength = hand_strength(other.row)
        self_strength = hand_strength(self.row)

        if self_strength.value < other_strength.value:
            return True
        elif self_strength.value > other_strength.value:
            return False
        else:  # same hand, have to compare ranks
            if self_strength in [PokerHand.PAIR, PokerHand.TRIPS,
                                 PokerHand.TWO_PAIR, PokerHand.FULL_HOUSE, PokerHand.QUADS]:
                self_freq = defaultdict(int)
                other_freq = defaultdict(int)
                for self_c in self.row:
                    self_freq[self_c.rank] += 1
                for other_c in other.row:
                    other_freq[other_c.rank] += 1

                self_ranks = [x[0].value for x in sorted(self_freq.items(), key=lambda x: x[1], reverse=True)]
                other_ranks = [x[0].value for x in sorted(other_freq.items(), key=lambda x: x[1], reverse=True)]
                return self_ranks < other_ranks
            else:
                self_ranks = sorted([c.rank.value for c in self.row], reverse=True)
                other_ranks = sorted([c.rank.value for c in other.row], reverse=True)
                return self_ranks < other_ranks

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def hand_strength(self):
        return hand_strength(self.row)


class OfcHand:
    def __init__(self, top=None, middle=None, bottom=None):
        if top:
            self.top = OfcRow(3, top)
        else:
            self.top = OfcRow(3)

        if middle:
            self.middle = OfcRow(5, middle)
        else:
            self.middle = OfcRow(5)

        if bottom:
            self.bottom = OfcRow(5, bottom)
        else:
            self.bottom = OfcRow(5)

    def __str__(self):
        return "{}_{}_{}".format(
            cards_to_str(self.top.row),
            cards_to_str(self.middle.row),
            cards_to_str(self.bottom.row)
        )

    def add_bottom(self, card):
        self.bottom.add_card(card)

    def add_middle(self, card):
        self.middle.add_card(card)

    def add_top(self, card):
        self.top.add_card(card)

    @property
    def total_cards(self):
        return self.top.total_cards + self.middle.total_cards + self.bottom.total_cards

    @property
    def completed(self):
        return self.top.completed and self.middle.completed and self.bottom.completed

    @property
    def foul(self):
        return self.completed and not (self.top <= self.middle <= self.bottom)

    def calculate_total_royalties(self):
        return royalties(self.bottom.row, Row.BOTTOM) + \
               royalties(self.middle.row, Row.MIDDLE) + \
               royalties(self.top.row, Row.TOP)

    def calculate_points(self, other):
        assert self.completed and other.completed
        if other.foul and self.foul:
            return 0
        elif other.foul:
            return royalties(self.bottom.row, Row.BOTTOM) + royalties(self.middle.row, Row.MIDDLE) + royalties(
                self.top.row,
                Row.TOP) + 6
        elif self.foul:
            return (royalties(other.bottom.row, Row.BOTTOM) + royalties(other.middle.row, Row.MIDDLE) + royalties(
                other.top.row,
                Row.TOP) + 6) * -1
        points = 0

        points += royalties(self.bottom.row, Row.BOTTOM) - royalties(other.bottom.row, Row.BOTTOM)
        if self.bottom > other.bottom:
            points += 1
        elif self.bottom < other.bottom:
            points -= 1

        points += royalties(self.middle.row, Row.MIDDLE) - royalties(other.middle.row, Row.MIDDLE)
        if self.middle > other.middle:
            points += 1
        elif self.middle < other.middle:
            points -= 1

        points += royalties(self.top.row, Row.TOP) - royalties(other.top.row, Row.TOP)
        if self.top > other.top:
            points += 1
        elif self.top < other.top:
            points -= 1

        if self.bottom > other.bottom and self.middle > other.middle and self.top > other.top:
            points += 3
        elif other.bottom > self.bottom and other.middle > self.middle and other.top > self.top:
            points -= 3

        return points
