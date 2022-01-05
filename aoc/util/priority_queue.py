import itertools
from heapq import heappush, heappop
from typing import Any


class PriorityQueue:
    """
    https://docs.python.org/3/library/heapq.html
    """
    REMOVED = '<removed-task>'  # placeholder for a removed task

    def __init__(self):
        self._pq = []
        self._entry_finder = {}
        self._counter = itertools.count()

    def push(self, value: Any, priority=0):
        if value in self._entry_finder:
            self._remove_task(value)

        count = next(self._counter)
        entry = [priority, count, value]
        self._entry_finder[value] = entry
        heappush(self._pq, entry)

    def _remove_task(self, value: Any):
        entry = self._entry_finder.pop(value)
        entry[-1] = PriorityQueue.REMOVED

    def pop(self) -> Any:
        while self._pq:
            _, __, value = heappop(self._pq)
            if value is not PriorityQueue.REMOVED:
                del self._entry_finder[value]
                return value

        raise KeyError('pop from an empty priority queue')

    def length(self) -> int:
        return len(self._entry_finder)
