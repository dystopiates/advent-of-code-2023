from functools import reduce
from typing import TypeVar, Callable, Any, Iterable


def readlines(filename: str) -> list[str]:
    with open(filename, 'r') as inp:
        return inp.read().splitlines()


T = TypeVar('T')

def maplines(callable: Callable[[str], T], filename: str) -> list[T]:
    return [callable(line) for line in readlines(filename)]


A = TypeVar('A')
B = TypeVar('B')
def maplist(callable: Callable[[A], B], items: Iterable[A]) -> list[B]:
    return list(map(callable, items))


def maplinetypes(line_s: str | list[str], *types: Callable[[str], Any]) -> list[Any] | list[list[Any]]:
    multiline = isinstance(line_s, list)
    lines = line_s if multiline else [line_s]

    mapped = []

    for line in lines:
        split = line.strip().split()
        assert len(split) == len(types)
        mapped.append(tuple(type(part) for type, part in zip(types, split)))

    if not multiline:
        mapped = mapped[0]

    return mapped


def multiply(items):
    return reduce(int.__mul__, items)
