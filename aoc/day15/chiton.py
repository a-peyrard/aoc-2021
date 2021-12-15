"""
--- Day 15: Chiton ---

You've almost reached the exit of the cave, but the walls are getting closer together. Your submarine can barely still
fit, though; the main problem is that the walls of the cave are covered in chitons, and it would be best not to bump any
 of them.
The cavern is large, but has a very low ceiling, restricting your motion to two dimensions. The shape of the cavern
resembles a square; a quick scan of chiton density produces a map of risk level throughout the cave (your puzzle input).
 For example:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581

You start in the top left position, your destination is the bottom right position, and you cannot move diagonally. The
number at each position is its risk level; to determine the total risk of an entire path, add up the risk levels of each
 position you enter (that is, don't count the risk level of your starting position unless you enter it; leaving it adds
 no risk to your total).
Your goal is to find a path with the lowest total risk. In this example, a path with the lowest total risk is
highlighted here:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581

The total risk of this path is 40 (the starting position is never entered, so its risk is not counted).
What is the lowest total risk of any path from the top left to the bottom right?

"""
import pprint
from collections import defaultdict
from heapq import heappush, heappop
from typing import List, NamedTuple, Any, Tuple

from aoc.util.matrix import serialize_matrix


DEBUG = False


class Coordinate(NamedTuple):
    x: int
    y: int


def shorted_path(matrix: List[List[int]]) -> int:
    costs = [
        [-1 for _ in row]
        for row in matrix
    ]
    costs[0][0] = 0

    height = len(matrix)
    width = len(matrix[0])

    target = Coordinate(width - 1, height - 1)

    to_analyze = PriorityQueue()
    to_analyze.push(Coordinate(0, 0), priority=0)
    while to_analyze.length() > 0:
        c = to_analyze.pop()
        if c == target:
            # this is our target
            break

        from_cost = costs[c.y][c.x]
        if c.y < height - 1:
            bottom = Coordinate(c.x, c.y + 1)
            new_assignment, cost = _assign_cost(
                costs=costs,
                current_coordinate=bottom,
                current_weight=matrix[bottom.y][bottom.x],
                from_cost=from_cost
            )
            if new_assignment:
                to_analyze.push(bottom, priority=cost)

        if c.y > 0:
            up = Coordinate(c.x, c.y - 1)
            new_assignment, cost = _assign_cost(
                costs=costs,
                current_coordinate=up,
                current_weight=matrix[up.y][up.x],
                from_cost=from_cost
            )
            if new_assignment:
                to_analyze.push(up, priority=cost)

        if c.x < width - 1:
            right = Coordinate(c.x + 1, c.y)
            new_assignment, cost = _assign_cost(
                costs=costs,
                current_coordinate=right,
                current_weight=matrix[right.y][right.x],
                from_cost=from_cost
            )
            if new_assignment:
                to_analyze.push(right, priority=cost)

        if c.x > 0:
            left = Coordinate(c.x - 1, c.y)
            new_assignment, cost = _assign_cost(
                costs=costs,
                current_coordinate=left,
                current_weight=matrix[left.y][left.x],
                from_cost=from_cost
            )
            if new_assignment:
                to_analyze.push(left, priority=cost)

    DEBUG and print(f'\n\ncost: \n{serialize_matrix(costs)}\n\n')

    return costs[-1][-1]


def _assign_cost(costs: List[List[int]],
                 current_coordinate: Coordinate,
                 current_weight: int,
                 from_cost: int) -> Tuple[bool, int]:
    existing_cost = costs[current_coordinate.y][current_coordinate.x]
    current_cost = from_cost + current_weight
    new_assignment = existing_cost == -1
    if new_assignment or existing_cost > current_cost:
        costs[current_coordinate.y][current_coordinate.x] = current_cost
        return True, current_cost

    return False, -1


class PriorityQueue:
    """
    https://docs.python.org/3/library/heapq.html
    """
    REMOVED = '<removed-task>'  # placeholder for a removed task

    def __init__(self):
        self._pq = []
        self._entry_finder = {}

    def push(self, value: Any, priority=0):
        if value in self._entry_finder:
            self._remove_task(value)
        entry = (priority, value)
        self._entry_finder[value] = entry
        heappush(self._pq, entry)

    def _remove_task(self, value: Any):
        entry = self._entry_finder.pop(value)
        entry[-1] = PriorityQueue.REMOVED

    def pop(self) -> Any:
        while self._pq:
            priority, value = heappop(self._pq)
            if value is not PriorityQueue.REMOVED:
                del self._entry_finder[value]
                return value

        raise KeyError('pop from an empty priority queue')

    def length(self) -> int:
        return len(self._entry_finder)
