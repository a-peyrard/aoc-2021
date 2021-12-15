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
from typing import List, NamedTuple

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

    paths = [Coordinate(0, 0)]
    while len(paths) > 0:
        c = paths.pop(0)
        from_cost = costs[c.y][c.x]
        if c.y < height - 1:
            bottom = Coordinate(c.x, c.y + 1)
            new_assignment = _assign_cost(
                costs=costs,
                current_coordinate=bottom,
                current_weight=matrix[bottom.y][bottom.x],
                from_cost=from_cost
            )
            if new_assignment:
                paths.append(bottom)

        if c.y > 0:
            up = Coordinate(c.x, c.y - 1)
            new_assignment = _assign_cost(
                costs=costs,
                current_coordinate=up,
                current_weight=matrix[up.y][up.x],
                from_cost=from_cost
            )
            if new_assignment:
                paths.append(up)

        if c.x < width - 1:
            right = Coordinate(c.x + 1, c.y)
            new_assignment = _assign_cost(
                costs=costs,
                current_coordinate=right,
                current_weight=matrix[right.y][right.x],
                from_cost=from_cost
            )
            if new_assignment:
                paths.append(right)

        if c.x > 0:
            left = Coordinate(c.x - 1, c.y)
            new_assignment = _assign_cost(
                costs=costs,
                current_coordinate=left,
                current_weight=matrix[left.y][left.x],
                from_cost=from_cost
            )
            if new_assignment:
                paths.append(left)

    DEBUG and print(f'\n\ncost: \n{serialize_matrix(costs)}\n\n')
    return costs[-1][-1]


def _assign_cost(costs: List[List[int]],
                 current_coordinate: Coordinate,
                 current_weight: int,
                 from_cost: int) -> bool:
    existing_cost = costs[current_coordinate.y][current_coordinate.x]
    current_cost = from_cost + current_weight
    new_assignment = existing_cost == -1
    if new_assignment or existing_cost > current_cost:
        costs[current_coordinate.y][current_coordinate.x] = current_cost
        return True

    return False
