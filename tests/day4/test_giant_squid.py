from collections.abc import Iterable
from typing import List, Tuple

from hamcrest import assert_that, equal_to

from aoc.day4.giant_squid import Grid, calculate_bingo_score
from aoc.util.input import parse_input_file


class TestCalculateBingoScore:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> Tuple[List[int], List[Grid]]:
        lines = list(lines)

        draw = list(map(int, lines[0].split(",")))
        grids = TestCalculateBingoScore._parse_grids(lines[2:])

        return draw, grids

    @staticmethod
    def _parse_grids(lines: Iterable[str]) -> List[Grid]:
        current = []
        grids = []
        for line in lines:
            tokens = list(map(int, line.split()))
            if not tokens:
                grids.append(current)
                current = []
                continue

            current.append(tokens)

        if current:
            grids.append(current)

        return grids

    def test_should_validate_given_sample(self):
        # GIVEN
        draw, grids = TestCalculateBingoScore._parse_input(
            lines="""7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""".splitlines(keepends=True)
        )

        # WHEN
        res = calculate_bingo_score(grids, draw)

        # THEN
        assert_that(res, equal_to(4512))

    def test_should_calculate_rate_for_input(self):
        # GIVEN
        draw, grids = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestCalculateBingoScore._parse_input
        )

        # WHEN
        res = calculate_bingo_score(grids, draw)

        # THEN
        assert_that(res, equal_to(49860))
