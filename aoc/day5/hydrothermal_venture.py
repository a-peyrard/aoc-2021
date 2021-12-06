"""
--- Day 5: Hydrothermal Venture ---

You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds,
so it would be best to avoid them if possible.
They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for
you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2

Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end
the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends.
In other words:

    An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.
So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....

In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of
lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 ->
2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.
To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the
above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.
Consider only horizontal and vertical lines. At how many points do at least two lines overlap?

"""
from typing import NamedTuple, Tuple, List

from aoc.util.matrix import initialize_matrix, IntMatrix


class Coordinate(NamedTuple):
    x: int
    y: int


Vent = Tuple[Coordinate, Coordinate]


def calculate_overlap(vents: List[Vent],
                      threshold: int = 2,
                      include_diagonals: bool = False) -> int:
    width, height = _get_matrix_size(vents)
    matrix = initialize_matrix(fill=0, row=height, col=width)

    res = 0
    for vent in vents:
        res += _draw_vent(matrix, vent, threshold, include_diagonals)

    return res


def _draw_vent(matrix: IntMatrix,
               vent: Vent,
               threshold: int,
               include_diagonals: bool) -> int:
    matching_threshold = 0
    if vent[0].x == vent[1].x:
        if vent[0].y < vent[1].y:
            min = vent[0].y
            max = vent[1].y
        else:
            min = vent[1].y
            max = vent[0].y

        for y in range(min, max + 1):
            matrix[y][vent[0].x] += 1
            if matrix[y][vent[0].x] == threshold:
                matching_threshold += 1
    elif vent[0].y == vent[1].y:
        if vent[0].x < vent[1].x:
            min = vent[0].x
            max = vent[1].x
        else:
            min = vent[1].x
            max = vent[0].x

        for x in range(min, max + 1):
            matrix[vent[0].y][x] += 1
            if matrix[vent[0].y][x] == threshold:
                matching_threshold += 1
    elif include_diagonals:
        if vent[0].x < vent[1].x:
            start = vent[0]
            end = vent[1]
        else:
            start = vent[1]
            end = vent[0]

        height_increment = 1 if end.y - start.y > 0 else -1
        y = start.y
        for x in range(start.x, end.x + 1):
            matrix[y][x] += 1
            if matrix[y][x] == threshold:
                matching_threshold += 1
            y += height_increment

    return matching_threshold


def _get_matrix_size(vents: List[Vent]) -> Tuple[int, int]:
    width = 0
    height = 0
    for vent in vents:
        for idx in range(2):
            if width < vent[idx].x:
                width = vent[idx].x
            if height < vent[idx].y:
                height = vent[idx].y

    return width + 1, height + 1
