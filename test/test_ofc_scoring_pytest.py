import pytest
from deck import parse_cards
import ofc_scoring


@pytest.mark.parametrize("hand,royalties", [
    (parse_cards(["2c", "2d"]), 0),  # pair
    (parse_cards(["2c", "2d", "8s", "3h", "3s"]), 0),  # two pair
    (parse_cards(["2c", "2d", "2s", "4d"]), 0),  # trips
    (parse_cards(["5c", "6d", "7c", "8d", "9c"]), 2),  # straight
    (parse_cards(["6d", "5d", "Ad", "Kd", "7d"]), 4),  # flush
    (parse_cards(["5c", "5d", "5s", "Ah", "Ac"]), 6),  # full house
    (parse_cards(["2c", "2d", "2s", "2h", "3s"]), 10),  # quads
    (parse_cards(["Ad", "2d", "3d", "4d", "5d"]), 15),  # straight flush
    (parse_cards(["Ad", "Kd", "Qd", "Jd", "Td"]), 25),  # royal flush
])
def test_bottom(hand, royalties):
    assert ofc_scoring.royalties(hand, ofc_scoring.Row.BOTTOM) == royalties


@pytest.mark.parametrize("hand,royalties", [
    (parse_cards(["2c", "2d"]), 0),  # pair
    (parse_cards(["2c", "2d", "8s", "3h", "3s"]), 0),  # two pair
    (parse_cards(["2c", "2d", "2s", "4d"]), 2),  # trips
    (parse_cards(["5c", "6d", "7c", "8d", "9c"]), 4),  # straight
    (parse_cards(["6d", "5d", "Ad", "Kd", "7d"]), 8),  # flush
    (parse_cards(["5c", "5d", "5s", "Ah", "Ac"]), 12),  # full house
    (parse_cards(["2c", "2d", "2s", "2h", "3s"]), 20),  # quads
    (parse_cards(["Ad", "2d", "3d", "4d", "5d"]), 30),  # straight flush
    (parse_cards(["Ad", "Kd", "Qd", "Jd", "Td"]), 50),  # royal flush
])
def test_middle(hand, royalties):
    assert ofc_scoring.royalties(hand, ofc_scoring.Row.MIDDLE) == royalties


@pytest.mark.parametrize("hand,royalties", [
    (parse_cards(["2c", "3d", "Ad"]), 0),  # no royalty ace high
    (parse_cards(["2c", "2d", "Ad"]), 0),  # no royalty pair
    (parse_cards(["6c", "6d", "Ad"]), 1),  # lower bound royalty pair
    (parse_cards(["7c", "7d", "Ad"]), 2),  # middle royalty pair
    (parse_cards(["Qc", "Qd", "Ad"]), 7 + 7.5),  # upper bound royalty pair
    (parse_cards(["Kc", "Kd", "Ad"]), 8 + 7.5),  # upper bound royalty pair
    (parse_cards(["Ac", "Kd", "Ad"]), 9 + 7.5),  # upper bound royalty pair
    (parse_cards(["2c", "2d", "2h"]), 10),  # trips
    (parse_cards(["6c", "6d", "6h"]), 14),  # trips
    (parse_cards(["Kc", "Kd", "Kh"]), 21),  # trips
    (parse_cards(["Ac", "Ad", "Ah"]), 22),  # trips
])
def test_top(hand, royalties):
    assert ofc_scoring.royalties(hand, ofc_scoring.Row.TOP) == royalties
