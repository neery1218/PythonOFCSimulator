from ofc_hand import OfcHand
from deck import parse_cards
from deck import parse_card
from hand_ev_estimator import Decision
from hand_ev_estimator import find_optimal_decision
from hand_ev_estimator import Placement
from ofc_scoring import Row


def _create_ofc_hand(top, middle, bottom):
    ofc_hand = OfcHand()

    if top:
        for c in parse_cards(top.split(" ")):
            ofc_hand.add_top(c)

    if middle:
        for c in parse_cards(middle.split(" ")):
            ofc_hand.add_middle(c)

    if bottom:
        for c in parse_cards(bottom.split(" ")):
            ofc_hand.add_bottom(c)

    return ofc_hand


def decision_finder(our_hand, their_hand, dead_cards, candidate_decisions, num_epochs):
    # parse decisions
    decisions = []
    for d in candidate_decisions:
        arr = d.split(" ")
        placements = []
        dead_cards_d = [c for c in dead_cards]
        for c, action in zip(arr[0::2], arr[1::2]):
            card = parse_card(c)
            if action == "top":
                placements.append(Placement(card=card, row=Row.TOP))
            elif action == "mid":
                placements.append(Placement(card=card, row=Row.MIDDLE))
            elif action == "bot":
                placements.append(Placement(card=card, row=Row.BOTTOM))
            elif action == "dead":
                dead_cards_d.append(card)
            else:
                raise AssertionError("wtf")

        decisions.append(Decision(placements=placements, dead_cards=dead_cards_d))

    return find_optimal_decision(
        our_hand=our_hand,
        their_hand=their_hand,
        decisions=decisions,
        num_epochs=num_epochs,
    )


def conflicting_draw_flush_q():
    # 2d Kc Ac
    our_hand = _create_ofc_hand(
        "Qs",
        "Ts Tc 9s 2d",
        "Kh Jh 8h 6h"
    )
    their_hand = _create_ofc_hand(
        "Qd 5d",
        "Ad 7s 7d 4d 4s",
        "Ac 8c 5c 2c"
    )
    dead_cards = parse_cards(["8d", "3c"])

    candidate_decisions = [
        "Qc top 9d mid 2h dead",
        "Qc top 2h bot 9d dead",
        "2h bot 9d mid Qc dead",
    ]
    placements_to_ev = decision_finder(
        our_hand=our_hand,
        their_hand=their_hand,
        dead_cards=dead_cards,
        candidate_decisions=candidate_decisions,
        num_epochs=10000
    )

    for placements, ev in placements_to_ev.items():
        s = "{} {} {} {}".format(placements[0].card, placements[0].row, placements[1].card, placements[1].row)
        print("{} : {}".format(s, ev))


def pair_or_q_top(): # TODO: not enough compute power
    # 2d Kc Ac
    our_hand = _create_ofc_hand(
        None,
        "9h 8c",
        "Ah Ad 5d",
    )
    their_hand = _create_ofc_hand(
        "Ks",
        "7c 2c",
        "6s 6c",
    )
    dead_cards = []

    candidate_decisions = [
        "Qh top 3h mid 3c dead",
        "3h mid 3c mid Qh dead",

    ]
    placements_to_ev = decision_finder(
        our_hand=our_hand,
        their_hand=their_hand,
        dead_cards=dead_cards,
        candidate_decisions=candidate_decisions,
        num_epochs=10000
    )

    for placements, ev in placements_to_ev.items():
        s = "{} {} {} {}".format(placements[0].card, placements[0].row, placements[1].card, placements[1].row)
        print("{} : {}".format(s, ev))


def T_top_or_mid():
    # 2d Kc Ac
    our_hand = _create_ofc_hand(
        None,
        "9c 9d",
        "Ac Ad 3s 3h 3d"
    )
    their_hand = _create_ofc_hand(
        "Qc",
        "Kd 4d",
        "Ts 9s 8h 2s",
    )
    dead_cards = parse_cards(["6c"])

    candidate_decisions = [
        "Th mid 5d mid 2h dead",
        "Th top 5d mid 2h dead"
    ]
    placements_to_ev = decision_finder(
        our_hand=our_hand,
        their_hand=their_hand,
        dead_cards=dead_cards,
        candidate_decisions=candidate_decisions,
        num_epochs=10000
    )

    for placements, ev in placements_to_ev.items():
        s = "{} {} {} {}".format(placements[0].card, placements[0].row, placements[1].card, placements[1].row)
        print("{} : {}".format(s, ev))


if __name__ == '__main__':
    # conflicting_draw_flush_q()
    # freeroll_or_88_top()
    # pair_or_q_top()
    T_top_or_mid()

