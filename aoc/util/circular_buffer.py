from typing import Optional, List


class CircularBuffer:
    def __init__(self,
                 length: int,
                 initial: Optional[List[int]] = None):
        self._index = 0
        self._length = length
        self._buf = initial or [0] * length
        if initial and len(initial) != length:
            raise ValueError('length and the initial values length are not the same!')

    def push(self, val: int) -> int:
        prev = self._buf[self._index]
        self._buf[self._index] = val
        self._index = (self._index + 1) % self._length
        return prev
