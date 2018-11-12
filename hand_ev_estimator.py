from itertools import combinations
from itertools import chain
from deck import Deck
from ofc_hand import OfcHand
from ofc_scoring import Row
from collections import namedtuple


NUM_EPOCHS = 10000
DRAWS_TO_CARDS = {
    1: 3,
    2: 5,
    3: 9,
    4: 9,
}


class HandEvEstimator:

    def __init__(self, our_ofc_hand, their_ofc_hand, dead_cards):
        self.our_ofc_hand = our_ofc_hand
        self.their_ofc_hand = their_ofc_hand

        self.deck = Deck()

        removal = [c for c in chain(
                dead_cards,
                self.our_ofc_hand.top.row,
                self.their_ofc_hand.top.row,
                self.our_ofc_hand.middle.row,
                self.their_ofc_hand.middle.row,
                self.our_ofc_hand.bottom.row,
                self.their_ofc_hand.bottom.row)]
        assert len(removal) == len(set(removal))
        self.deck.remove_cards(removal)
        assert len(self.deck.deck_of_cards) == 52 - len(removal)

        assert self.our_ofc_hand.total_cards in [5, 7, 9, 11]
        assert self.their_ofc_hand.total_cards in [5, 7, 9, 11]

        self.our_draws_remaining = (13 - self.our_ofc_hand.total_cards) // 2
        self.their_draws_remaining = (13 - self.their_ofc_hand.total_cards) // 2

        assert abs(self.our_draws_remaining - self.their_draws_remaining) <= 1

    def estimate(self, num_epochs=NUM_EPOCHS):
        running_sum = 0
        iterations = 0
        num_our_cards = DRAWS_TO_CARDS[self.our_draws_remaining]
        print("Using {} cards".format(num_our_cards))
        num_their_cards = DRAWS_TO_CARDS[self.their_draws_remaining]
        for _ in range(num_epochs):
            if iterations % 100 == 0:
                print(iterations)
            cards = self.deck.choose(num_our_cards + num_their_cards)
            our_cards = cards[:num_our_cards]
            their_cards = cards[num_our_cards:]

            our_completed_hand = self.arrange_best_hand(
                self.our_ofc_hand, our_cards)
            their_completed_hand = self.arrange_best_hand(
                self.their_ofc_hand, their_cards)
            points = our_completed_hand.calculate_points(their_completed_hand)

            iterations += 1
            running_sum += points

        return running_sum / iterations

    @classmethod
    def arrange_best_hand(cls, ofc_hand, cards):
        best_ofc_hand = None
        best_ofc_hand_royalties = -1

        top_cards_remaining = 3 - ofc_hand.top.total_cards
        middle_cards_remaining = 5 - ofc_hand.middle.total_cards
        bottom_cards_remaining = 5 - ofc_hand.bottom.total_cards

        cards_set = set(cards)

        top_iter = combinations(cards_set, top_cards_remaining) if top_cards_remaining > 0 else 'e'
        num = 0
        for top_cards in top_iter:
            remaining_cards = cards_set - set(top_cards) if top_cards != 'e' else cards_set
            middle_iter = combinations(remaining_cards, middle_cards_remaining) if middle_cards_remaining > 0 else 'e'

            for middle_cards in middle_iter:
                remaining_cards_2 = remaining_cards - set(middle_cards) if middle_cards != 'e' else remaining_cards
                bottom_iter = combinations(remaining_cards_2, bottom_cards_remaining) if bottom_cards_remaining > 0 else 'e'

                for bottom_cards in bottom_iter:
                    num += 1
                    add_top = list(top_cards) if top_cards != 'e' else []
                    add_middle = list(middle_cards) if middle_cards != 'e' else []
                    add_bottom = list(bottom_cards) if bottom_cards != 'e' else []
                    tmp_ofc_hand = OfcHand(
                        ofc_hand.top.row + add_top,
                        ofc_hand.middle.row + add_middle,
                        ofc_hand.bottom.row + add_bottom,
                    )

                    tmp_ofc_hand_royalties = tmp_ofc_hand.calculate_total_royalties()
                    if best_ofc_hand is None:
                        best_ofc_hand = tmp_ofc_hand
                    if not tmp_ofc_hand.foul and tmp_ofc_hand_royalties > best_ofc_hand_royalties:
                        best_ofc_hand = tmp_ofc_hand
                        best_ofc_hand_royalties = tmp_ofc_hand_royalties
        return best_ofc_hand


Decision = namedtuple("Decision", ["placements", "dead_cards"])
Placement = namedtuple("Placement", ["card", "row"])


def find_optimal_decision(our_hand, their_hand, decisions, num_epochs=NUM_EPOCHS):
    decision_to_ev = dict()
    for decision in decisions:
        tmp_ofc_hand = OfcHand(
            our_hand.top.row,
            our_hand.middle.row,
            our_hand.bottom.row,
        )

        for placement in decision.placements:
            if placement.row == Row.TOP:
                tmp_ofc_hand.add_top(placement.card)
            elif placement.row == Row.MIDDLE:
                tmp_ofc_hand.add_middle(placement.card)
            elif placement.row == Row.BOTTOM:
                tmp_ofc_hand.add_bottom(placement.card)
            else:
                raise AssertionError("wtf")
        hand_ev_estimator = HandEvEstimator(
            our_ofc_hand=tmp_ofc_hand,
            their_ofc_hand=their_hand,
            dead_cards=decision.dead_cards,
        )

        ev = hand_ev_estimator.estimate(num_epochs=num_epochs)
        decision_to_ev[tuple(decision.placements)] = ev

    return decision_to_ev
