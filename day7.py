from functools import cmp_to_key

from utils import readlines


def simplify_hand(hand: str) -> dict[str, int]:
    d = {}

    for c in hand:
        d[c] = d.get(c, 0) + 1

    return d


def grade_hand_type(hand: str, wild_jokers: bool) -> int:
    # 0: five of a kind
    # 1: four of a kind
    # 2: full house
    # 3: three of a kind
    # 4: two pair
    # 5: one pair
    # 6: high card
    if wild_jokers:
        wild = hand.count('J')
        s = simplify_hand(hand.replace('J', ''))
    else:
        wild = 0
        s = simplify_hand(hand)

    counts = list(s.values())
    counts.sort(reverse=True)

    if wild == 5:
        counts = [5]
    else:
        counts[0] += wild

    counts = tuple(counts)

    return {
        (5,): 0,
        (4, 1): 1,
        (3, 2): 2,
        (3, 1, 1): 3,
        (2, 2, 1): 4,
        (2, 1, 1, 1): 5,
        (1, 1, 1, 1, 1): 6
    }[counts]


def get_same_type_hand_comparator(strength: str):
    def compare_same_type_hands(left: str, right: str) -> int:
        for l, r in zip(left, right):
            if l != r:
                return strength.index(r) - strength.index(l)

        return 0

    return compare_same_type_hands


def rank_hands(
        hands: list[str],
        wild_jokers: bool,
        strength: str
) -> list[str]:
    comparator = get_same_type_hand_comparator(strength)
    types = [[] for _ in range(7)]

    for hand in hands:
        types[grade_hand_type(hand, wild_jokers)].append(hand)

    for major_ranked in types:
        major_ranked.sort(key=cmp_to_key(comparator))

    ranked = []
    for type in types[::-1]:
        ranked += type

    return ranked


def play(lines: list[str], wild_jokers: bool, strength: str):
    hand_bids = [(l.split()[0], int(l.split()[1])) for l in lines]
    ranked = {
        hand: i + 1 for i, hand in enumerate(rank_hands([hb[0] for hb in hand_bids], wild_jokers, strength))
    }

    value = 0
    for hand, bid in hand_bids:
        value += ranked[hand] * bid

    print(value)


def part1(lines: list[str]):
    play(lines, False, 'AKQJT98765432')


def part2(lines: list[str]):
    play(lines, True, 'AKQT98765432J')


if __name__ == '__main__':
    part1(readlines('day7.test.input'))
