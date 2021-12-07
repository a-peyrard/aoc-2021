from typing import Iterable

from hamcrest import assert_that, equal_to

from aoc.day7.the_treachery_of_wales import calculate_amount_of_fuel, calculate_amount_of_fuel_2
from aoc.util.input import parse_input_file


class TestCalculateAmountOfFuel:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> Iterable[int]:
        line = next(lines.__iter__())
        return map(int, line.split(","))

    def test_should_validate_given_sample(self):
        # GIVEN
        positions = TestCalculateAmountOfFuel._parse_input(
            lines="""16,1,2,0,4,2,7,1,2,14
""".splitlines(keepends=True)
        )

        # WHEN
        res = calculate_amount_of_fuel(positions)

        # THEN
        assert_that(res, equal_to(37))

    def test_should_count_fuel_for_input(self):
        # GIVEN
        positions = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestCalculateAmountOfFuel._parse_input
        )

        # WHEN
        res = calculate_amount_of_fuel(positions)

        # THEN
        assert_that(res, equal_to(347449))

    def test_should_validate_given_sample_part2(self):
        # GIVEN
        positions = TestCalculateAmountOfFuel._parse_input(
            lines="""16,1,2,0,4,2,7,1,2,14
""".splitlines(keepends=True)
        )

        # WHEN
        res = calculate_amount_of_fuel_2(positions)

        # THEN
        assert_that(res, equal_to(168))

    def test_should_count_fuel_for_input_part2(self):
        # GIVEN
        positions = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestCalculateAmountOfFuel._parse_input
        )

        # WHEN
        res = calculate_amount_of_fuel_2(positions)

        # THEN
        assert_that(res, equal_to(98039527))
