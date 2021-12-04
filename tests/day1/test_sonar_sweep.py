from typing import List, Iterable

from hamcrest import equal_to, assert_that

from aoc.day1.sonar_sweep import count_increases, count_increases_by_batches
from aoc.util.input import parse_input_file


class TestCountIncreases:
    @staticmethod
    def _parse_lines(lines: Iterable[str]) -> List[int]:
        return list(map(int, lines))

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
        measurements = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=self._parse_lines
        )

        # WHEN
        res = count_increases(measurements)

        # THEN
        assert_that(res, equal_to(1759))

    def test_should_validate_given_sample_for_part2(self):
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
        res = count_increases_by_batches(measurements, batch_size=3)

        # THEN
        assert_that(res, equal_to(5))

    def test_should_validate_input_for_part2(self):
        # GIVEN
        measurements = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=self._parse_lines
        )

        # WHEN
        res = count_increases_by_batches(measurements, batch_size=3)

        # THEN
        assert_that(res, equal_to(1805))
