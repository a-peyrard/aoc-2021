from collections.abc import Iterable
from typing import Tuple

from hamcrest import assert_that, equal_to

from aoc.day2.dive import Direction, calculate_position, calculate_position_with_aim
from aoc.util.input import parse_input_file


class TestCalculatePosition:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> Iterable[Tuple[Direction, int]]:
        return (
            TestCalculatePosition._parse_line(line)
            for line in lines
        )

    @staticmethod
    def _parse_line(line: str) -> Tuple[Direction, int]:
        tokens = line.split()
        return Direction[tokens[0]], int(tokens[1])

    def test_should_calculate_position_for_sample(self):
        # GIVEN
        instructions = TestCalculatePosition._parse_input(
            lines="""forward 5
down 5
forward 8
up 3
down 8
forward 2""".splitlines(keepends=True)
        )

        # WHEN
        res = calculate_position(instructions)

        # THEN
        assert_that(res, equal_to(150))

    def test_should_calculate_position_for_input(self):
        # GIVEN
        instructions = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestCalculatePosition._parse_input
        )

        # WHEN
        res = calculate_position(instructions)

        # THEN
        assert_that(res, equal_to(1840243))

    def test_should_calculate_position_for_sample_part2(self):
        # GIVEN
        instructions = TestCalculatePosition._parse_input(
            lines="""forward 5
down 5
forward 8
up 3
down 8
forward 2""".splitlines(keepends=True)
        )

        # WHEN
        res = calculate_position_with_aim(instructions)

        # THEN
        assert_that(res, equal_to(900))

    def test_should_calculate_position_for_input_part2(self):
        # GIVEN
        instructions = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestCalculatePosition._parse_input
        )

        # WHEN
        res = calculate_position_with_aim(instructions)

        # THEN
        assert_that(res, equal_to(1727785422))
