import re

from utils import maplist, readlines

card_re = re.compile(r'Card +(\d+): (.+) \| (.+)')
Card = tuple[int, list[int], list[int]]


def parse_card(line: str) -> Card:
    card_id, winning, guesses = card_re.fullmatch(line).groups()

    return (
        card_id,
        maplist(int, winning.split()),
        maplist(int, guesses.split())
    )


def score_card(winning: list[int], guesses: list[int]) -> int:
    winning = set(winning)
    winning_guesses = [guess for guess in guesses if guess in winning]

    if len(winning_guesses) == 0:
        return 0
    return 2 ** (len(winning_guesses) - 1)


def sum_card_scores(cards: list[Card]) -> int:
    return sum(score_card(winning, guesses) for _, winning, guesses in cards)


def play_and_count_cards(cards: list[Card]) -> int:
    counts = [1] * len(cards)

    for i, (_, winning, guesses) in enumerate(cards):
        winning = set(winning)
        winning_guesses = [guess for guess in guesses if guess in winning]
        for j in range(len(winning_guesses)):
            counts[i + j + 1] += counts[i]

    return sum(counts)


def part1(lines: list[str]):
    print(sum_card_scores(maplist(parse_card, lines)))


def part2(lines: list[str]):
    print(play_and_count_cards(maplist(parse_card, lines)))


if __name__ == '__main__':
    part2(readlines('day4.input'))
