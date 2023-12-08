import re

import math

from utils import readlines, maplist

node_re = re.compile(r'(.*?) = \((.*?), (.*?)\)')


def build_graph(nodes: list[str]) -> dict[str, tuple[str, str]]:
    return {
        node: (left, right)
        for node, left, right in map(lambda n: node_re.fullmatch(n).groups(), nodes)
    }


def follow_to(graph: dict[str, tuple[str, str]], directions: list[int], starting: list[str] = None) -> int:
    nodes = starting or list(filter(lambda n: n.endswith('A'), graph.keys()))
    ends = [None for _ in nodes]

    for i, node in enumerate(nodes):
        index = 0
        steps = 0

        while not node.endswith('Z'):
            node = graph[node][directions[index]]

            index = (index + 1) % len(directions)
            steps += 1

        ends[i] = steps

    return math.lcm(*ends)


def part1(graph: dict[str, tuple[str, str]], instructions: list[int]):
    print(follow_to(graph, instructions, starting=['AAA']))


def part2(graph: dict[str, tuple[str, str]], instructions: list[int]):
    print(follow_to(graph, instructions))


if __name__ == '__main__':
    lines_ = readlines('day8.input')
    part2(build_graph(lines_[2:]), maplist(lambda c: 'LR'.index(c), lines_[0]))
