import re
from typing import Optional

from utils import maplist, readlines


class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def intersects(self, other: 'Range') -> bool:
        s1, d1 = self
        s2, d2 = other

        return s2 <= s1 < d2 or s1 <= s2 < d1

    def __iter__(self):
        yield from (self.start, self.end)

    @property
    def len(self):
        return self.end - self.start

    def __repr__(self) -> str:
        return f'<Range [{self.start}, {self.end})>'


def sum_range_lens(ranges: list[Range]) -> int:
    return sum(r.len for r in ranges)


class RangeMap:
    def __init__(self, src: Range, dst: Range):
        assert src.len == dst.len
        self.src = src
        self.dst = dst

    def remap(self, range: Range) -> tuple[Optional[Range], Range, Optional[Range]]:
        assert self.src.intersects(range)

        mapped = [None, None, None]

        # unmapped prefix
        if range.start < self.src.start:
            mapped[0] = Range(range.start, self.src.start)

        # mapped mid-section
        offset = max(range.start, self.src.start) - self.src.start
        len = min(range.end, self.src.end) - max(range.start, self.src.start)
        mapped[1] = Range(
            self.dst.start + offset,
            self.dst.start + offset + len
        )
        assert self.dst.start <= mapped[1].start < mapped[1].end <= self.dst.end

        # unmapped postfix
        if range.end > self.src.end:
            mapped[2] = Range(self.src.end, range.end)

        assert sum(map(lambda r: 0 if r is None else r.len, mapped)) == range.len

        return tuple(mapped)

    @staticmethod
    def from_values(dst: int, src: int, len: int) -> 'RangeMap':
        src = Range(src, src + len)
        dst = Range(dst, dst + len)

        return RangeMap(src, dst)

    def __repr__(self):
        return f'<RangeMap {repr(self.src)} -> {repr(self.dst)}'


class Almanac:
    def __init__(self, seeds: list[Range], mappings: dict[str, tuple[str, list[RangeMap]]]):
        self.seeds = seeds
        self.mappings = mappings

    def follow_mappings(self, seeds: Range, final_key: str) -> list[Range]:
        key = 'seed'
        values = [seeds]

        while key != final_key:
            key, mappings = self.mappings[key]
            unremapped = values[:]
            remapped = []

            for mapping in mappings:
                for range in unremapped[:]:
                    if mapping.src.intersects(range):
                        prefix, remap, postfix = mapping.remap(range)
                        unremapped_insert = list(filter(lambda e: e is not None, [prefix, postfix]))

                        remapped.append(remap)
                        unremapped.remove(range)
                        unremapped += unremapped_insert

                        assert sum_range_lens(unremapped + remapped) == sum_range_lens(values)

            values = unremapped + remapped

        return values

    @staticmethod
    def from_lines(lines: list[str]) -> 'Almanac':
        assert lines[0].startswith('seeds:')
        map_re = re.compile(r'(.+?)-to-(.*?) map:')

        seeds = [Range(int(start), int(start) + int(len_)) for start, len_ in re.findall(r'(\d+) +(\d+)', lines[0])]

        mappings = {}
        mapping = []

        for line in lines[1:]:
            if len(line) == 0:
                continue

            if (map_header := map_re.fullmatch(line)) is not None:
                src, dst = map_header.groups()
                mapping = []
                mappings[src] = (dst, mapping)

            else:
                mapping.append(RangeMap.from_values(*maplist(int, line.split())))

        return Almanac(seeds, mappings)


def part2(lines: list[str]):
    almanac = Almanac.from_lines(lines)

    mapped = []
    for seedrange in almanac.seeds:
        mapped += almanac.follow_mappings(seedrange, 'location')

    print(sum(seedrange.len for seedrange in almanac.seeds))
    print(sum(locrange.len for locrange in mapped))
    print(min(map(lambda m: m.start, mapped)))


if __name__ == '__main__':
    part2(readlines('day5.input'))
