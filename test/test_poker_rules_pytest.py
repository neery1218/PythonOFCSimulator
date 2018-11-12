import pytest
from deck import parse_cards
import poker_rules
from poker_rules import PokerHand


@pytest.mark.parametrize("hand,expected", [
    (parse_cards(["Ad", "Kd", "Qd", "Jd", "Td"]), True),
    (parse_cards(["Ad", "2d", "3d", "4d", "5d"]), False),  # straight flush but not royal
])
def test_royal_flush(hand, expected):
    if expected:
        assert poker_rules.hand_strength(hand) == PokerHand.ROYAL_FLUSH
    else:
        assert poker_rules.hand_strength(hand) != PokerHand.ROYAL_FLUSH


@pytest.mark.parametrize("hand,expected", [
    (parse_cards(["Ad", "2d", "3d", "4d", "5d"]), True),
    (parse_cards(["2d", "6d", "4d", "5d", "3d"]), True),
    (parse_cards(["Ad", "6d", "4d", "5d", "3d"]), False),
    (parse_cards(["Ac", "2d", "3c", "4d", "5c"]), False),  # straight
    (parse_cards(["6d", "5d", "Ad", "Kd", "7d"]), False),  # flush
])
def test_straight_flush(hand, expected):
    if expected:
        assert poker_rules.hand_strength(hand) == PokerHand.STRAIGHT_FLUSH
    else:
        assert poker_rules.hand_strength(hand) != PokerHand.STRAIGHT_FLUSH


@pytest.mark.parametrize("hand,expected", [
    (parse_cards(["5c", "5d", "5s", "5h", "Ah"]), True),
    (parse_cards(["2c", "2d", "2s", "2h"]), True),
    (parse_cards(["2c", "2d", "2s", "3h", "3s"]), False),  # full house
    (parse_cards(["2c", "2d", "2s", "3h"]), False),  # trips
])
def test_quads(hand, expected):
    if expected:
        assert poker_rules.hand_strength(hand) == PokerHand.QUADS
    else:
        assert poker_rules.hand_strength(hand) != PokerHand.QUADS


@pytest.mark.parametrize("hand,expected", [
    (parse_cards(["5c", "5d", "5s", "Ah", "Ac"]), True),
    (parse_cards(["2c", "2d", "2s", "3h", "3d"]), True),
    (parse_cards(["2c", "2d", "2s", "2h", "3s"]), False),  # quads
    (parse_cards(["2c", "2d", "2s"]), False),  # trips
])
def test_full_house(hand, expected):
    if expected:
        assert poker_rules.hand_strength(hand) == PokerHand.FULL_HOUSE
    else:
        assert poker_rules.hand_strength(hand) != PokerHand.FULL_HOUSE


@pytest.mark.parametrize("hand,expected", [
    (parse_cards(["6d", "5d", "Ad", "Kd", "7d"]), True),
    (parse_cards(["6d", "5d", "Ad", "Kd", ]), False),  # flush draw
    (parse_cards(["2c", "2d", "2s", "2h", "3s"]), False),  # not a flush
])
def test_flush(hand, expected):
    if expected:
        assert poker_rules.hand_strength(hand) == PokerHand.FLUSH
    else:
        assert poker_rules.hand_strength(hand) != PokerHand.FLUSH

@pytest.mark.parametrize("hand,expected", [
    (parse_cards(["Ac", "2d", "3c", "4d", "5c"]), True),  # edge case 1
    (parse_cards(["Ac", "Kd", "Qc", "Jd", "Tc"]), True),  # edge case 2
    (parse_cards(["5c", "6d", "7c", "8d", "9c"]), True),
    (parse_cards(["6c", "5d", "7c", "8d", "9c"]), True),
    (parse_cards(["6d", "5d", "7d", "8d", "Td"]), False),  # not a straight
])
def test_straight(hand, expected):
    if expected:
        assert poker_rules.hand_strength(hand) == PokerHand.STRAIGHT
    else:
        assert poker_rules.hand_strength(hand) != PokerHand.STRAIGHT


@pytest.mark.parametrize("hand,expected", [
    (parse_cards(["2c", "2d", "2s"]), True),
    (parse_cards(["2c", "2d", "2s", "4d"]), True),
    (parse_cards(["2c", "2d", "2s", "3d", "4d"]), True),
    (parse_cards(["5c", "5d", "5s", "Ah", "Ac"]), False),  # full house
    (parse_cards(["2c", "2d", "2s", "2h", "3s"]), False),  # quads
    (parse_cards(["2c", "2d", "8s", "3h", "3s"]), False),  # two pair
])
def test_trips(hand, expected):
    if expected:
        assert poker_rules.hand_strength(hand) == PokerHand.TRIPS
    else:
        assert poker_rules.hand_strength(hand) != PokerHand.TRIPS


@pytest.mark.parametrize("hand,expected", [
    (parse_cards(["2c", "2d", "8s", "3h", "3s"]), True),
    (parse_cards(["2c", "2d", "3h", "3s"]), True),
    (parse_cards(["2c", "2d", "2s", "4d"]), False),  # trips
    (parse_cards(["2c", "2d", "2s"]), False),  # trips
    (parse_cards(["5c", "5d", "5s", "Ah", "Ac"]), False),  # full house
    (parse_cards(["2c", "2d", "2s", "2h", "3s"]), False),  # quads
    (parse_cards(["2c", "2d", "8s", "4h", "3s"]), False),  # pair
    (parse_cards(["2c", "2d"]), False),  # pair
])
def test_two_pair(hand, expected):
    if expected:
        assert poker_rules.hand_strength(hand) == PokerHand.TWO_PAIR
    else:
        assert poker_rules.hand_strength(hand) != PokerHand.TWO_PAIR


@pytest.mark.parametrize("hand,expected", [
    (parse_cards(["2c", "2d"]), True),
    (parse_cards(["2c", "2d", "8s"]), True),
    (parse_cards(["2c", "2d", "8s", "4h"]), True),
    (parse_cards(["2c", "2d", "8s", "3h", "3s"]), False),  # two pair
    (parse_cards(["2c", "2d", "3h", "3s"]), False),  # two pair
    (parse_cards(["2c", "2d", "2s", "4d"]), False),  # trips
    (parse_cards(["5c", "5d", "5s", "Ah", "Ac"]), False),  # full house
    (parse_cards(["2c", "2d", "2s", "2h", "3s"]), False),  # quads
])
def test_pair(hand, expected):
    if expected:
        assert poker_rules.hand_strength(hand) == PokerHand.PAIR
    else:
        assert poker_rules.hand_strength(hand) != PokerHand.PAIR


@pytest.mark.parametrize("hand, strength", [
    (parse_cards(["Ad", "2d", "3d", "4d", "5d"]), PokerHand.STRAIGHT_FLUSH),  # straight flush
    (parse_cards(["2c", "2d"]), PokerHand.PAIR),  # pair
    (parse_cards(["2c", "2d", "8s", "3h", "3s"]), PokerHand.TWO_PAIR),  # two pair
    (parse_cards(["2c", "2d", "2s", "4d"]), PokerHand.TRIPS),  # trips
    (parse_cards(["5c", "6d", "7c", "8d", "9c"]), PokerHand.STRAIGHT),  # straight
    (parse_cards(["6d", "5d", "Ad", "Kd", "7d"]), PokerHand.FLUSH),  # flush
    (parse_cards(["5c", "5d", "5s", "Ah", "Ac"]), PokerHand.FULL_HOUSE),  # full house
    (parse_cards(["2c", "2d", "2s", "2h", "3s"]), PokerHand.QUADS),  # quads
    (parse_cards(["Ad", "Kd", "Qd", "Jd", "Td"]), PokerHand.ROYAL_FLUSH),  # royal flush
])
def test_hand_strength(hand, strength):
    assert poker_rules.hand_strength(hand) == strength
