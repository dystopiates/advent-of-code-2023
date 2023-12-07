from collections import Counter

from utils import readlines, maplinetypes


def grade_hand_type(hand: str, wild_jokers: bool) -> str:
    if wild_jokers:
        hand = hand.replace('J', Counter(hand).most_common()[0][0])

    counts = [c[1] for c in Counter(hand).most_common()]

    return ''.join(counts).ljust(5, '0')


def generate_hand_value(hand: str, wild_jokers: bool, strengths: str) -> str:
    return grade_hand_type(hand, wild_jokers) + ''.join('0123456789ABCDEF'[strengths.rindex(c)] for c in hand)


def play(lines: list[str], wild_jokers: bool, strengths: str):
    hand_bids = maplinetypes(lines, str, int)
    ranked = [generate_hand_value(hand, wild_jokers, strengths) for hand, _ in hand_bids]
    ranked.sort(key=lambda r: r[0])

    return sum((i + 1) * bid for i, (_, bid) in enumerate(ranked))


def part1(lines: list[str]):
    print(play(lines, False, 'AKQJT98765432'))


def part2(lines: list[str]):
    print(play(lines, True, 'AKQT98765432J'))


if __name__ == '__main__':
    part1(readlines('day7.test.input'))
