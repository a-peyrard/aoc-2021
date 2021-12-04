import os
from typing import Any, Callable, List, TypeVar

T = TypeVar('T')


def parse_input_file(origin: str,
                     filename: str,
                     callback: Callable[[List[str]], T]) -> T:
    with open(os.path.join(os.path.dirname(origin), filename)) as f:
        return callback(f.readlines())
