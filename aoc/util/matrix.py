from typing import List, TypeVar, ClassVar

T = TypeVar('T')

IntMatrix = List[List[int]]


def initialize_matrix(fill: T, row: int, col: int = None) -> List[List[T]]:
    col = col if col is not None else row
    return [
        [
            fill
            for _ in range(col)
        ]
        for _ in range(row)
    ]


def serialize_matrix(matrix: List[List[int]]) -> str:
    return "\n".join((
        " ".join(map(str, row))
        for row in matrix
    ))
