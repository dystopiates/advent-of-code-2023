import re
from typing import Any

from utils import maplist, readlines


class IntMap:
    def __init__(self):
        self.ranges: list[tuple[Any, int, int]] = []

    def update(self, dst_start: int, src_start: int, range_length: int):
        self.ranges.append((
            range(src_start, src_start + range_length),
            src_start,
            dst_start
        ))

    def __getitem__(self, item):
        assert isinstance(item, int)

        for range_, src, dst in self.ranges:
            if item in range_:
                return dst + (item - src)

        return item


class Almanac:
    def __init__(self, seeds: list[int], mappings: dict[str, tuple[str, IntMap]]):
        self.seeds = seeds
        self.mappings = mappings

    def follow_mappings(self, seed_number: int, final_key: str) -> int:
        key = 'seed'
        value = seed_number

        while key != final_key:
            key, mapping = self.mappings[key]
            value = mapping[value]

        return value

    @staticmethod
    def from_lines(lines: list[str]) -> 'Almanac':
        assert lines[0].startswith('seeds:')
        map_re = re.compile(r'(.+?)-to-(.*?) map:')

        seeds = maplist(int, lines[0].split(': ')[1].split())
        mappings = {}
        mapping = IntMap()

        for line in lines[1:]:
            if len(line) == 0:
                continue

            if (map_header := map_re.fullmatch(line)) is not None:
                src, dst = map_header.groups()
                mapping = IntMap()
                mappings[src] = (dst, mapping)

            else:
                mapping.update(*maplist(int, line.split()))

        return Almanac(seeds, mappings)


def part1(lines: list[str]):
    almanac = Almanac.from_lines(lines)

    min_seed = None
    min_loc = float('inf')
    for seed in almanac.seeds:
        location = almanac.follow_mappings(seed, 'location')

        if location < min_loc:
            min_seed, min_loc = seed, location

    print(f'seed: {min_seed}, loc: {min_loc}')


if __name__ == '__main__':
    part1(readlines('day5.input'))
