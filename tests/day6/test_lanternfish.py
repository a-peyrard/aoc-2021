from typing import Iterable

from hamcrest import assert_that, equal_to

from aoc.day6.lanternfish import count_lanternfish
from aoc.util.input import parse_input_file


class TestCountLanternfish:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> Iterable[int]:
        line = next(lines.__iter__())
        return map(int, line.split(","))

    def test_should_validate_given_sample(self):
        # GIVEN
        fishes = TestCountLanternfish._parse_input(
            lines="""3,4,3,1,2
""".splitlines(keepends=True)
        )

        # WHEN
        res = count_lanternfish(fishes, days=80)

        # THEN
        assert_that(res, equal_to(5934))

    def test_should_validate_given_sub_sample(self):
        # GIVEN
        fishes = TestCountLanternfish._parse_input(
            lines="""3,4,3,1,2
""".splitlines(keepends=True)
        )

        # WHEN
        res = count_lanternfish(fishes, days=18)

        # THEN
        assert_that(res, equal_to(26))

    def test_should_validate_given_sub_sample_day2(self):
        # GIVEN
        fishes = TestCountLanternfish._parse_input(
            lines="""3,4,3,1,2
""".splitlines(keepends=True)
        )

        # WHEN
        res = count_lanternfish(fishes, days=2)

        # THEN
        assert_that(res, equal_to(6))

    def test_should_validate_given_sub_sample_day5(self):
        # GIVEN
        fishes = TestCountLanternfish._parse_input(
            lines="""3,4,3,1,2
""".splitlines(keepends=True)
        )

        # WHEN
        res = count_lanternfish(fishes, days=5)

        # THEN
        assert_that(res, equal_to(10))

    def test_should_count_fishes_for_input(self):
        # GIVEN
        fishes = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestCountLanternfish._parse_input
        )

        # WHEN
        res = count_lanternfish(fishes, days=80)

        # THEN
        assert_that(res, equal_to(371379))

    def test_should_validate_given_part2_sample(self):
        # GIVEN
        fishes = TestCountLanternfish._parse_input(
            lines="""3,4,3,1,2
""".splitlines(keepends=True)
        )

        # WHEN
        res = count_lanternfish(fishes, days=256)

        # THEN
        assert_that(res, equal_to(26984457539))

    def test_should_count_fishes_for_input_part2(self):
        # GIVEN
        fishes = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestCountLanternfish._parse_input
        )

        # WHEN
        res = count_lanternfish(fishes, days=256)

        # THEN
        assert_that(res, equal_to(1674303997472))
