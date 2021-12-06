from collections.abc import Iterable
from typing import Tuple, List

from hamcrest import equal_to, assert_that

from aoc.day3.binary_diagnostic import calculate_rate, calculate_life_support_rating
from aoc.util.input import parse_input_file


class TestCalculateRate:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> Tuple[List[int], int]:
        lines_li = list(lines)
        return [int(line, 2) for line in lines], len(lines_li[0].strip())

    def test_should_validate_given_sample(self):
        # GIVEN
        numbers, length = TestCalculateRate._parse_input(
            lines="""00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".splitlines(keepends=True)
        )

        # WHEN
        res = calculate_rate(numbers, length)

        # THEN
        assert_that(res, equal_to(198))

    def test_should_calculate_rate_for_input(self):
        # GIVEN
        numbers, length = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestCalculateRate._parse_input
        )

        # WHEN
        res = calculate_rate(numbers, length)

        # THEN
        assert_that(res, equal_to(3009600))

    def test_should_validate_given_sample_for_life_support_rating(self):
        # GIVEN
        numbers, length = TestCalculateRate._parse_input(
            lines="""00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".splitlines(keepends=True)
        )

        # WHEN
        res = calculate_life_support_rating(numbers, length)

        # THEN
        assert_that(res, equal_to(230))

    def test_should_calculate_rate_for_input_part2(self):
        # GIVEN
        numbers, length = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestCalculateRate._parse_input
        )

        # WHEN
        res = calculate_life_support_rating(numbers, length)

        # THEN
        assert_that(res, equal_to(6940518))
