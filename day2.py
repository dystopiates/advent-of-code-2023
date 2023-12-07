import re
from typing import Callable

from utils import multiply

CUBES_re = r'\d+ \w+'
ROUND_re = rf'{CUBES_re}(, {CUBES_re})*'
GAME_re = rf'Game \d+: {ROUND_re}(; {ROUND_re})*'

CubeSet = dict[str, int]


def cubeset_from_line(line: str) -> CubeSet:
    line = line.strip()
    assert re.fullmatch(ROUND_re, line)

    revealed = {}

    for revelation in line.split(', '):
        num, key = revelation.split()

        assert key not in revealed
        revealed[key] = int(num)

    return revealed


def minimize_cubeset(cubesets: list[CubeSet]) -> CubeSet:
    min_cubeset = {}

    for cubeset in cubesets:
        for key, count in cubeset.items():
            min_cubeset[key] = max(min_cubeset.get(key, 0), count)

    return min_cubeset


class Game:
    def __init__(self, game_id: str, rounds: list[CubeSet]):
        self.game_id = game_id
        self.rounds = rounds

    @staticmethod
    def from_line(line: str) -> 'Game':
        line = line.strip()

        assert re.fullmatch(GAME_re, line)

        game_id, rounds = line.split(': ')

        game_id = game_id.split()[1]
        rounds = [cubeset_from_line(round) for round in rounds.split('; ')]

        return Game(game_id, rounds)


def is_possible(available: CubeSet) -> Callable[[Game], bool]:
    def _is_possible(game: Game) -> bool:
        for round in game.rounds:
            for key, count in round.items():
                if count > available.get(key, 0):
                    return False

        return True

    return _is_possible


def filter_by_restraints(games: list[Game], restraints: CubeSet) -> list[Game]:
    return [game for game in filter(is_possible(restraints), games)]


def sum_matching(games: list[Game], restraints: CubeSet) -> int:
    return sum((int(game.game_id) for game in filter_by_restraints(games, restraints)))


def part1(games: list[Game]):
    _restraints = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    print(sum_matching(games, _restraints))


def part2(games: list[Game]):
    print(sum(
        multiply(minimize_cubeset(game.rounds).values())
        for game in games
    ))


if __name__ == '__main__':
    with open('day2.input', 'r') as inp:
        _games = list(map(Game.from_line, inp.readlines()))

    #part1(_games)
    part2(_games)
