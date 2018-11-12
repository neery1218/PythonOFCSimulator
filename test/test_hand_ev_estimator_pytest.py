import pytest
from ofc_hand import OfcHand
from deck import parse_cards
from hand_ev_estimator import HandEvEstimator


def _create_ofc_hand(top, middle, bottom):
    ofc_hand = OfcHand()

    for c in parse_cards(top.split(" ")):
        ofc_hand.add_top(c)

    for c in parse_cards(middle.split(" ")):
        ofc_hand.add_middle(c)

    for c in parse_cards(bottom.split(" ")):
        ofc_hand.add_bottom(c)

    return ofc_hand


def test_hand_ev_estimator_golden():
    pass
    """
    our_hand = _create_ofc_hand(
        "Ah",
        "Jh Jc Th Tc 4d",
        "Kh Kc 5h"
    )
    their_hand = _create_ofc_hand(
        "Qh As Qc",
        "Js Jd Ts",
        "Kd Ks 5s"
    )

    dead_cards = parse_cards(["7d", "7h", "7c"])
    estimator = HandEvEstimator(
        our_ofc_hand=our_hand,
        their_ofc_hand=their_hand,
        dead_cards=dead_cards)

    print(estimator.estimate())
    """
