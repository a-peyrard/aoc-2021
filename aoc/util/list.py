from functools import reduce
from operator import add
from typing import TypeVar, Iterable, List

T = TypeVar("T")


def flat_map(iterable: Iterable[Iterable[T]]) -> List[T]:
    return [
        t
        for ts in iterable
        for t in ts
    ]


def last(iterable: Iterable[T],
         default_value: T) -> T:
    _last = default_value
    for _last in iterable:
        pass

    return _last
