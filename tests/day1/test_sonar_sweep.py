from typing import List, Iterable

from hamcrest import equal_to, assert_that

from aoc.day1.sonar_sweep import count_increases
from aoc.util.input import parse_input_file


class TestCountIncreases:
    def test_should_validate_given_sample(self):
        # GIVEN
        measurements = [
            199,
            200,
            208,
            210,
            200,
            207,
            240,
            269,
            260,
            263
        ]

        # WHEN
        res = count_increases(measurements)

        # THEN
        assert_that(res, equal_to(7))

    def test_should_validate_input(self):
        # GIVEN
        def _parse_lines(lines: Iterable[str]) -> List[int]:
            return list(map(int, lines))

        measurements = parse_input_file(
            origin=__file__,
            filename='input1.txt',
            callback=_parse_lines
        )

        # WHEN
        res = count_increases(measurements)

        # THEN
        assert_that(res, equal_to(1759))
