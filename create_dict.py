from deck import *
from itertools import permutations
from ofc_hand import *

cards = []
rows = []

for suit in Suit:
    for rank in Rank:
        cards.append(Card(rank, suit))

for comb in permutations(cards, 3):
    row = OfcRow(3, comb)
    rows.append(row)

for comb in permutations(cards, 5):
    row = OfcRow(5, comb)
    rows.append(row)

rows.sort()
print(len(rows))

with open("hand_strength.csv", 'w+') as f:
    counter = 0
    for i, row in enumerate(rows):
        if i > 0 and row > rows[i - 1]:
            counter += 1

        f.write(",".join([cards_to_str(row.row), str(counter), str(hand_strength(row.row).value)]))
        f.write("\n")




