import pytest
from deck import parse_cards
from ofc_hand import OfcRow
from ofc_hand import OfcHand
from deck import Card
from deck import Suit
from deck import Rank


def test_add_card_golden():
    row = OfcRow(3)
    for c in parse_cards(["2c", "2d", "2h"]):
        row.add_card(c)

    assert row.completed


def test_add_card_too_many():
    row = OfcRow(3)
    for c in parse_cards(["2c", "2d", "2h"]):
        row.add_card(c)

    with pytest.raises(AssertionError):
        row.add_card(Card(Rank.ACE, Suit.DIAMONDS))


@pytest.mark.parametrize("row_1, row_2, expected_lt, expected_le", [
    (
            parse_cards(["Ad", "Kd", "Qd", "Jd", "Td"]),
            parse_cards(["9d", "Kd", "Qd", "Jd", "Td"]),
            False,
            False,
    ), (
            parse_cards(["9d", "Kd", "Qd", "Jd", "Td"]),
            parse_cards(["Ad", "Kd", "Qd", "Jd", "Td"]),
            True,
            True,
    ), (
            parse_cards(["Ad", "Kd", "Qd", "Jd", "Td"]),
            parse_cards(["Ad", "Kd", "Qd", "Jd", "Td"]),
            False,
            True,
    ), (  # other is higher straight flush
            parse_cards(["9d", "8d", "Qd", "Jd", "Td"]),
            parse_cards(["9d", "Kd", "Qd", "Jd", "Td"]),
            True,
            True,
    ), (  # full house
            parse_cards(["8d", "8h", "8c", "Jd", "Jd"]),
            parse_cards(["3d", "3c", "3h", "Ad", "Ah"]),
            False,
            False,
    ), (  # two pair
            parse_cards(["8d", "8h", "3c", "3d", "Ad"]),
            parse_cards(["Jc", "Jh", "Th", "Th", "4c"]),
            True,
            True,
    ), (  # two pair
            parse_cards(["Jc", "Jh", "Th", "Th", "4c"]),
            parse_cards(["8d", "8h", "3c", "3d", "Ad"]),
            False,
            False,
    ), (  # pair
            parse_cards(["8d", "8h", "Ad"]),
            parse_cards(["Jc", "Jh", "4c"]),
            True,
            True,
    ), (  # same pair
            parse_cards(["8d", "8h", "Ad"]),
            parse_cards(["8c", "8s", "Kd"]),
            False,
            False,
    ), (  # same pair
            parse_cards(["8c", "8s", "Kd"]),
            parse_cards(["8d", "8h", "Ad"]),
            True,
            True,
    ), (  # same pair same kicker
            parse_cards(["8c", "8s", "Kd"]),
            parse_cards(["8d", "8h", "Kh"]),
            False,
            True,
    ),
])
def test_comparators(row_1, row_2, expected_lt, expected_le):
    ofc_row_1 = OfcRow(5)
    ofc_row_2 = OfcRow(5)

    for c_1, c_2 in zip(row_1, row_2):
        ofc_row_1.add_card(c_1)
        ofc_row_2.add_card(c_2)

    assert ((ofc_row_1 < ofc_row_2) == expected_lt)
    assert ((ofc_row_1 >= ofc_row_2) == (not expected_lt))

    assert ((ofc_row_1 <= ofc_row_2) == expected_le)
    assert ((ofc_row_1 > ofc_row_2) == (not expected_le))


def test_ofc_hand_golden():
    ofc_hand = OfcHand()

    for c in parse_cards(["2c", "2d", "2h"]):
        ofc_hand.add_top(c)

    for c in parse_cards(["6h", "6d", "6c", "6s", "As"]):
        ofc_hand.add_middle(c)

    for c in parse_cards(["8h", "8d", "8c", "8s", "9s"]):
        ofc_hand.add_bottom(c)

    assert ofc_hand.completed


def test_foul():
    ofc_hand = OfcHand()

    for c in parse_cards(["2c", "2d", "2h"]):
        ofc_hand.add_top(c)

    for c in parse_cards(["Ah", "Ah", "6c", "6s", "As"]):
        ofc_hand.add_middle(c)

    for c in parse_cards(["Th", "8d", "8c", "8s", "9s"]):
        ofc_hand.add_bottom(c)

    assert ofc_hand.foul


def test_no_foul():
    ofc_hand = OfcHand()

    for c in parse_cards(["2c", "2d", "2h"]):
        ofc_hand.add_top(c)

    for c in parse_cards(["6h", "6d", "6c", "6s", "As"]):
        ofc_hand.add_middle(c)

    for c in parse_cards(["8h", "8d", "8c", "8s", "9s"]):
        ofc_hand.add_bottom(c)

    assert not ofc_hand.foul


def _create_ofc_hand(top, middle, bottom):
    ofc_hand = OfcHand()

    for c in parse_cards(top.split(" ")):
        ofc_hand.add_top(c)

    for c in parse_cards(middle.split(" ")):
        ofc_hand.add_middle(c)

    for c in parse_cards(bottom.split(" ")):
        ofc_hand.add_bottom(c)

    return ofc_hand


@pytest.mark.parametrize("hand_1, hand_2, points", [
    (
            _create_ofc_hand(
                "Ah Ac Qc",
                "Jh Jc Th Tc Ac",
                "Kh Kc 5h 5c 2d"
            ),
            _create_ofc_hand(
                "Qh Ac Qc",
                "Js Jd Ts Td Ah",
                "Kd Ks 5s 5d 2c"
            ),
            3,
    ),
    (
            _create_ofc_hand(  # aces up top
                "Ah Ac Qc",
                "Jh Jc Th Tc Ac",
                "Kh Kc 5h 5c 2d"
            ),
            _create_ofc_hand(  # foul
                "Qh Ac Qc",
                "Js Jd Ts Td Ah",
                "Kd Ks 6s 5d 2c"
            ),
            22.5,
    ),
    (
            _create_ofc_hand(  # foul
                "Qh Ac Qc",
                "Js Jd Ts Td Ah",
                "Kd Ks 6s 5d 2c"
            ),
            _create_ofc_hand(  # aces up top
                "Ah Ad Qc",
                "Jh Jc Th Tc As",
                "Kh Kc 5h 5c 2d"
            ),
            -22.5,
    ),
    (
            _create_ofc_hand(  # scooped but no foul
                "Kh Ah Qc",
                "Js Jd Ts Td Ah",
                "Kd Ks 6s 5d 2c"
            ),
            _create_ofc_hand(  # aces up top
                "Ad Ac Qh",
                "2d 2c 2h 4h 6h",
                "Kh Kc Kd 5c 5d"
            ),
            -30.5,
    ),
    (
            _create_ofc_hand(
                "Kd Kc Ad",
                "5s 5h 5d 4s 3s",
                "7s 7d 7h 7c 2d"
            ),
            _create_ofc_hand(
                "Ah Ac Qc",
                "2d 2c 4c 4h 6h",
                "3h 3c 3s 5c 5d"
            ),
            6,
    ),
    (
            _create_ofc_hand(
                "Ah Ac Qc",
                "5s 5h 5d 4s 3s",
                "7s 7d 7h 7c 2d"
            ),
            _create_ofc_hand(
                "Kd Kc Ad",
                "2d 2c 4c 4h 6h",
                "3h 3c 3s 5c 5d"
            ),
            13,
    ),
])
def test_calculate_points(hand_1, hand_2, points):
    assert hand_1.calculate_points(hand_2) == points
