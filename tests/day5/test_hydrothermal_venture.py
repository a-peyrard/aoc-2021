from collections.abc import Iterable
from typing import List

from hamcrest import assert_that, equal_to

from aoc.day5.hydrothermal_venture import Vent, Coordinate, calculate_overlap
from aoc.util.input import parse_input_file


class TestCalculateOverlap:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> List[Vent]:
        return [
            TestCalculateOverlap._parse_line(line)
            for line in lines
        ]

    @staticmethod
    def _parse_line(line: str) -> Vent:
        raw_coordinates = line.split(" -> ")
        return TestCalculateOverlap._parse_coordinate(raw_coordinates[0]), \
               TestCalculateOverlap._parse_coordinate(raw_coordinates[1])

    @staticmethod
    def _parse_coordinate(raw_coordinate: str) -> Coordinate:
        tokens = raw_coordinate.split(",")
        return Coordinate(int(tokens[0]), int(tokens[1]))

    def test_should_validate_given_sample(self):
        # GIVEN
        vents = TestCalculateOverlap._parse_input(
            lines="""0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".splitlines(keepends=True)
        )

        # WHEN
        res = calculate_overlap(vents, threshold=2)

        # THEN
        assert_that(res, equal_to(5))

    def test_should_calculate_overlap_for_input(self):
        # GIVEN
        vents = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestCalculateOverlap._parse_input
        )

        # WHEN
        res = calculate_overlap(vents, threshold=2)

        # THEN
        assert_that(res, equal_to(6267))

    def test_should_validate_given_sample_part2(self):
        # GIVEN
        vents = TestCalculateOverlap._parse_input(
            lines="""0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".splitlines(keepends=True)
        )

        # WHEN
        res = calculate_overlap(vents, threshold=2, include_diagonals=True)

        # THEN
        assert_that(res, equal_to(12))

    def test_should_calculate_overlap_for_input_part2(self):
        # GIVEN
        vents = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestCalculateOverlap._parse_input
        )

        # WHEN
        res = calculate_overlap(vents, threshold=2, include_diagonals=True)

        # THEN
        assert_that(res, equal_to(20196))
