import re

from utils import readlines, multiply

XY = tuple[int, int]
partnum_re = re.compile(r'(\d+)')


def get_partnumber_index(schematic: list[str], x: int, y: int) -> XY:
    while x > 0 and schematic[y][x - 1] in '1234567890':
        x -= 1

    return x, y


def get_adjacent_number_indices(schematic: list[str], xy: XY) -> set[XY]:
    partnumbers: set[XY] = set()

    x, y = xy
    max_y = len(schematic)
    max_x = len(schematic[0])

    for y_ in range(max(0, y - 1), min(max_y, y + 1) + 1):
        for x_ in range(max(0, x - 1), min(max_x, x + 1) + 1):
            if schematic[y_][x_] in '1234567890':
                partnumbers.add(get_partnumber_index(schematic, x_, y_))

    return partnumbers


def read_part_number(schematic: list[str], xy: XY) -> int:
    x, y = xy
    return int(partnum_re.findall(schematic[y][x:])[0])


def get_part_number_locations(schematic: list[str]) -> set[XY]:
    part_number_locations: set[XY] = set()

    for y, row in enumerate(schematic):
        for x, c in enumerate(row):
            if c not in '0123456789.':
                part_number_locations = part_number_locations.union(get_adjacent_number_indices(schematic, (x, y)))

    return part_number_locations


def get_gear_ratio_muls(schematic: list[str]) -> list[int]:
    ratio_muls: list[int] = []

    for y, row in enumerate(schematic):
        for x, c in enumerate(row):
            if c == '*' and len(ratio := get_adjacent_number_indices(schematic, (x, y))) == 2:
                ratio_muls.append(multiply(*(read_part_number(schematic, xy) for xy in ratio)))

    return ratio_muls


def sum_part_numbers(schematic: list[str]) -> int:
    return sum(read_part_number(schematic, xy) for xy in get_part_number_locations(schematic))


def part1(lines: list[str]):
    print(sum_part_numbers(lines))


def part2(lines: list[str]):
    print(sum(get_gear_ratio_muls(lines)))


if __name__ == '__main__':
    part2(readlines('day3.input'))
