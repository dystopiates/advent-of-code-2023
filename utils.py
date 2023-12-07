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


def mapline(line: str, *types: Callable[[str], Any]) -> list[Any]:
    split = line.strip().split()

    assert len(split) == len(types)

    return [type(part) for type, part in zip(types, split)]
