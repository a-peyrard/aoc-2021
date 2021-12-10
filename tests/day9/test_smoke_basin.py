from typing import Iterable, List

from hamcrest import assert_that, equal_to

from aoc.day9.smoke_basin import count_low_point
from aoc.util.input import parse_input_file


class TestSmokeBasin:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> List[List[int]]:
        return [
            [
                int(c)
                for c in line.strip()
            ]
            for line in lines
        ]

    def test_should_validate_given_sample(self):
        # GIVEN
        matrix = TestSmokeBasin._parse_input(
            lines="""2199943210
3987894921
9856789892
8767896789
9899965678
""".splitlines(keepends=True)
        )

        # WHEN
        res = count_low_point(matrix)

        # THEN
        assert_that(res, equal_to(15))

    def test_should_count_low_points_for_input(self):
        # GIVEN
        matrix = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestSmokeBasin._parse_input
        )

        # WHEN
        res = count_low_point(matrix)

        # THEN
        assert_that(res, equal_to(570))
