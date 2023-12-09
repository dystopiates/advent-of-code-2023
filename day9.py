from utils import readlines, maplist


def diffsequence(sequence: list[int]) -> list[int]:
    return [r - l for l, r in zip(sequence, sequence[1:])]


def derive_to_zero(sequence: list[int]) -> list[list[int]]:
    history = [sequence]

    while any(history[-1]):
        history.append(diffsequence(history[-1]))

    return history


def backfill_history(history: list[list[int]]) -> list[list[int]]:
    history[-1].append(0)
    for upper, lower in zip(history[::-1][1:], history[::-1]):
        upper.append(upper[-1] + lower[-1])

    return history


def infill_history(history: list[list[int]]) -> list[list[int]]:
    history[-1].insert(0, 0)
    for upper, lower in zip(history[::-1][1:], history[::-1]):
        upper.insert(0, upper[0] - lower[0])

    return history


def part1(sequences: list[list[int]]):
    backfilled = [backfill_history(derive_to_zero(sequence)) for sequence in sequences]

    print(sum(h[0][-1] for h in backfilled))


def part2(sequences: list[list[int]]):
    backfilled = [infill_history(derive_to_zero(sequence)) for sequence in sequences]

    print(sum(h[0][0] for h in backfilled))


if __name__ == '__main__':
    part2([maplist(int, line.split()) for line in readlines('day9.input')])
