from utils import readlines, maplist, multiply


def enumerate_wins(time: int, distance: int) -> list[int]:
    wins = []

    for btime in range(1, time + 1):
        bdistance = btime * (time - btime)

        if bdistance > distance:
            wins.append(btime)

    return wins


def part1(lines: list[str]):
    assert len(lines) == 2
    assert lines[0].startswith('Time:')
    assert lines[1].startswith('Distance:')

    times = maplist(int, lines[0][len('Time:'):].strip().split())
    distances = maplist(int, lines[1][len('Distance:'):].strip().split())

    margins = []
    for time, distance in zip(times, distances):
        margins.append(len(enumerate_wins(time, distance)))

    print(multiply(margins))


def part2(lines: list[str]):
    time = int(lines[0][5:].replace(' ', ''))
    distance = int(lines[1][9:].replace(' ', ''))

    print(len(enumerate_wins(time, distance)))


if __name__ == '__main__':
    part2(readlines('day6.input'))
