from typing import List, TypeVar

T = TypeVar('T')


def initialize_matrix(fill: T, row: int, col: int = None) -> List[List[T]]:
    col = col if col is not None else row
    return [
        [
            fill
            for _ in range(col)
        ]
        for _ in range(row)
    ]
