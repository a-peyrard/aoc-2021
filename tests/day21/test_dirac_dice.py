from typing import Iterable, Tuple

import pytest
from hamcrest import assert_that, equal_to

from aoc.day21.dirac_dice import solution_1, solution_2
from aoc.util.input import parse_input_file


class TestDiracDice:
    @staticmethod
    def _given_sample() -> Tuple[int, int]:
        return TestDiracDice._parse_input(
            lines="""Player 1 starting position: 4
Player 2 starting position: 8
""".splitlines(keepends=True)
        )

    @staticmethod
    def _parse_input(lines: Iterable[str]) -> Tuple[int, int]:
        lines_li = list(lines)

        return int(lines_li[0][28:]), int(lines_li[1][28:])

    def test_should_compute_solution_1_for_given_sample(self):
        # GIVEN
        player_1, player_2 = TestDiracDice._given_sample()

        # WHEN
        res = solution_1(player_1, player_2)

        # THEN
        assert_that(res, equal_to(739785))

    def test_should_compute_solution_1_for_given_input(self):
        # GIVEN
        player_1, player_2 = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestDiracDice._parse_input
        )

        # WHEN
        res = solution_1(player_1, player_2)

        # THEN
        assert_that(res, equal_to(921585))

    @pytest.mark.slow
    def test_should_compute_solution_2_for_given_sample(self):
        # GIVEN
        player_1, player_2 = TestDiracDice._given_sample()

        # WHEN
        player_1_wins, player_2_wins = solution_2(player_1, player_2)

        # THEN
        assert_that(player_1_wins, equal_to(444356092776315))
        assert_that(player_2_wins, equal_to(341960390180808))

    @pytest.mark.slow
    def test_should_compute_solution_2_for_given_input(self):
        # GIVEN
        player_1, player_2 = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestDiracDice._parse_input
        )

        # WHEN
        player_1_wins, player_2_wins = solution_2(player_1, player_2)

        # THEN
        assert_that(max(player_1_wins, player_2_wins), equal_to(911090395997650))
