from functools import cmp_to_key
from typing import Callable

from utils import readlines, maplinetypes


def simplify_hand(hand: str) -> dict[str, int]:
    return {c: hand.count(c) for c in set(hand)}


def grade_hand_type(hand: str, wild_jokers: bool) -> int:
    if wild_jokers:
        wild = hand.count('J')
        if wild == 5:
            return 0  # five of a kind
        s = simplify_hand(hand.replace('J', ''))
    else:
        wild = 0
        s = simplify_hand(hand)

    counts = list(s.values())
    counts.sort(reverse=True)
    counts[0] += wild
    counts = tuple(counts)

    return {
        (5,): 0,            # 0: five of a kind
        (4, 1): 1,          # 1: four of a kind
        (3, 2): 2,          # 2: full house
        (3, 1, 1): 3,       # 3: three of a kind
        (2, 2, 1): 4,       # 4: two pair
        (2, 1, 1, 1): 5,    # 5: one pair
        (1, 1, 1, 1, 1): 6  # 6: high card
    }[counts]


def get_same_type_hand_comparator(strength: str) -> Callable[[tuple[str, int], tuple[str, int]], int]:
    def compare_same_type_hands(left: tuple[str, int], right: tuple[str, int]) -> int:
        for l, r in zip(left[0], right[0]):
            if l != r:
                return strength.index(r) - strength.index(l)

        return 0

    return compare_same_type_hands


def rank_hands(hands: list[tuple[str, int]], wild_jokers: bool, strength: str) -> list[str]:
    comparator = get_same_type_hand_comparator(strength)
    types = [[] for _ in range(7)]

    for hand in hands:
        types[grade_hand_type(hand[0], wild_jokers)].append(hand)

    for major_ranked in types:
        major_ranked.sort(key=cmp_to_key(comparator))

    ranked = []
    for type in types[::-1]:
        ranked += type

    return ranked


def play(lines: list[str], wild_jokers: bool, strength: str):
    hand_bids = maplinetypes(lines, str, int)
    ranked = rank_hands(hand_bids, wild_jokers, strength)

    return sum((i + 1) * bid for i, (_, bid) in enumerate(ranked))


def part1(lines: list[str]):
    print(play(lines, False, 'AKQJT98765432'))


def part2(lines: list[str]):
    print(play(lines, True, 'AKQT98765432J'))


if __name__ == '__main__':
    part1(readlines('day7.test.input'))
