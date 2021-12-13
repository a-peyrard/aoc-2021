from typing import Iterable, List, Tuple

import pytest
from hamcrest import assert_that, equal_to

from aoc.day13.transparent_origami import Paper
from aoc.util.input import parse_input_file


class TestTransparentOrigami:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> Tuple[List[Tuple[int, int]], List[Tuple[str, int]]]:
        coordinates = []
        instructions = []
        in_coordinates = True
        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                in_coordinates = False
                continue
            if in_coordinates:
                coordinates.append(TestTransparentOrigami._parse_coordinate(line))
            else:
                instructions.append(TestTransparentOrigami._parse_instruction(line))

        return coordinates, instructions

    @staticmethod
    def _parse_coordinate(line: str) -> Tuple[int, int]:
        tokens = line.split(",")
        return int(tokens[0]), int(tokens[1])

    @staticmethod
    def _parse_instruction(line: str) -> Tuple[str, int]:
        tokens = line[11:].split("=")
        return tokens[0], int(tokens[1])

    def test_should_count_dots_for_first_given_sample(self):
        # GIVEN
        coordinates, instructions = TestTransparentOrigami._parse_input(
            lines="""6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""".splitlines(keepends=True)
        )

        # WHEN
        res = Paper(coordinates).fold(instructions[0]).count_dots()

        # THEN
        assert_that(res, equal_to(17))

    def test_should_draw_correct_figure_after_first_instruction_first_given_sample(self):
        # GIVEN
        coordinates, instructions = TestTransparentOrigami._parse_input(
            lines="""6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""".splitlines(keepends=True)
        )

        # WHEN
        figure = Paper(coordinates).fold(instructions[0]).serialize()

        # THEN
        print(f"figure: \n{figure}")
        assert_that(
            figure,
            equal_to("""#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
..........."""))

    def test_should_draw_correct_figure_after_all_for_first_given_sample(self):
        # GIVEN
        coordinates, instructions = TestTransparentOrigami._parse_input(
            lines="""6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""".splitlines(keepends=True)
        )

        # WHEN
        paper = Paper(coordinates)
        for instruction in instructions:
            paper.fold(instruction)
        figure = paper.serialize()

        # THEN
        print(f"figure: \n{figure}")
        assert_that(
            figure,
            equal_to("""#####
#...#
#...#
#...#
#####
.....
....."""))

    def test_should_count_dots_for_input(self):
        # GIVEN
        coordinates, instructions = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestTransparentOrigami._parse_input
        )

        # WHEN
        res = Paper(coordinates).fold(instructions[0]).count_dots()

        # THEN
        assert_that(res, equal_to(669))

    @pytest.mark.slow
    def test_should_draw_figure_for_input(self):
        # GIVEN
        coordinates, instructions = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestTransparentOrigami._parse_input
        )

        # WHEN
        paper = Paper(coordinates)
        for instruction in instructions:
            paper.fold(instruction)
        figure = paper.serialize(padding=1)

        # THEN
        print(f"figure: \n{figure}")
        assert_that(figure, equal_to(""" # . . # . # # # # . # # # # . # # # # . . # # . . # . . # . . # # . . . . # # .
 # . . # . # . . . . # . . . . . . . # . # . . # . # . . # . # . . # . . . . # .
 # . . # . # # # . . # # # . . . . # . . # . . . . # . . # . # . . . . . . . # .
 # . . # . # . . . . # . . . . . # . . . # . . . . # . . # . # . . . . . . . # .
 # . . # . # . . . . # . . . . # . . . . # . . # . # . . # . # . . # . # . . # .
 . # # . . # # # # . # . . . . # # # # . . # # . . . # # . . . # # . . . # # . ."""))
