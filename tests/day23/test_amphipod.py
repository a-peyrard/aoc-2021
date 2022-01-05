from typing import Iterable, List, Optional

import pytest
from hamcrest import assert_that, equal_to

# noinspection PyProtectedMember
from aoc.day23.amphipod import State, organize, serialize_state, STEPS, _move_amphipod, _possible_next_states, \
    _heuristic, _sum_distances
from aoc.util.input import parse_input_file


class TestAmphipod:
    @staticmethod
    def _given_sample() -> State:
        return TestAmphipod._parse_input(
            lines="""#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
""".splitlines(keepends=True)
        )

    @staticmethod
    def _parse_input(lines: Iterable[str]) -> State:
        lines_li = list(lines)
        state: List[Optional[str]] = [None] * 15
        state[0] = TestAmphipod._parse_cell(lines_li[1][1])
        state[1] = TestAmphipod._parse_cell(lines_li[1][2])
        state[2] = TestAmphipod._parse_cell(lines_li[2][3])
        state[3] = TestAmphipod._parse_cell(lines_li[3][3])
        state[4] = TestAmphipod._parse_cell(lines_li[1][4])
        state[5] = TestAmphipod._parse_cell(lines_li[2][5])
        state[6] = TestAmphipod._parse_cell(lines_li[3][5])
        state[7] = TestAmphipod._parse_cell(lines_li[1][6])
        state[8] = TestAmphipod._parse_cell(lines_li[2][7])
        state[9] = TestAmphipod._parse_cell(lines_li[3][7])
        state[10] = TestAmphipod._parse_cell(lines_li[1][8])
        state[11] = TestAmphipod._parse_cell(lines_li[2][9])
        state[12] = TestAmphipod._parse_cell(lines_li[3][9])
        state[13] = TestAmphipod._parse_cell(lines_li[1][10])
        state[14] = TestAmphipod._parse_cell(lines_li[1][11])

        return tuple(state)

    @staticmethod
    def _parse_cell(val: str) -> Optional[str]:
        if val == ".":
            return None

        return val

    def test_should_parse_and_serialize_given_example(self):
        # GIVEN
        state = TestAmphipod._given_sample()

        # WHEN
        res = serialize_state(state)

        # THEN
        assert_that(res, equal_to("""#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""))

    def test_should_parse_and_serialize_custom_state(self):
        # GIVEN
        state = TestAmphipod._parse_input(
            lines="""#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########
""".splitlines(keepends=True)
        )

        # WHEN
        res = serialize_state(state)

        # THEN
        assert_that(res, equal_to("""#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########
"""))

    def test_should_define_symmetrical_steps(self):
        # GIVEN
        steps = STEPS

        # WHENS & THENS
        for y in range(len(STEPS)):
            for x in range(len(STEPS[y])):
                assert_that(steps[y][x], equal_to(steps[x][y]))

    def test_should_move_amphipod_example_1(self):
        # GIVEN
        state = TestAmphipod._given_sample()

        # WHEN
        next_state = _move_amphipod("B", 8, 4, state)

        # THEN
        assert_that(serialize_state(next_state), equal_to("""#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########
"""))

    def test_should_move_amphipod_example_2(self):
        # GIVEN
        state = TestAmphipod._given_sample()

        # WHEN
        next_state = _move_amphipod("B", 2, 14, state)

        # THEN
        assert_that(serialize_state(next_state), equal_to("""#############
#..........B#
###.#C#B#D###
  #A#D#C#A#
  #########
"""))

    def test_should_move_amphipod_example_3(self):
        # GIVEN
        state = TestAmphipod._given_sample()

        # WHEN
        next_state = _move_amphipod("B", 2, 14, state)
        next_state = _move_amphipod("C", 5, 0, next_state)

        # THEN
        assert_that(serialize_state(next_state), equal_to("""#############
#C.........B#
###.#.#B#D###
  #A#D#C#A#
  #########
"""))

    def test_should_get_possible_next_states_example_1(self):
        # GIVEN
        state = TestAmphipod._given_sample()

        # WHEN
        next_states = _possible_next_states(state)

        # THEN
        assert_that(len(next_states), equal_to(28))

    def test_should_get_possible_next_states_example_2(self):
        # GIVEN
        state = TestAmphipod._given_sample()

        # WHEN
        next_states = _possible_next_states(state)

        # THEN
        expected_state = TestAmphipod._parse_input(
            lines="""#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########
""".splitlines(keepends=True)
        )
        assert_that(next_states.get(expected_state), equal_to(40))

    def test_should_get_heuristic_for_perfect_state(self):
        # GIVEN
        state = TestAmphipod._parse_input(
            lines="""#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
""".splitlines(keepends=True)
        )

        # WHEN
        val = _heuristic(state)

        # THEN
        assert_that(val, equal_to(0))

    def test_should_organize_for_almost_done_state(self):
        # GIVEN
        state = TestAmphipod._parse_input(
            lines="""#############
#A.........D#
###.#B#C#.###
  #A#B#C#D#
  #########
""".splitlines(keepends=True)
        )

        # WHEN
        res = organize(state)

        # THEN
        assert_that(res, equal_to(3003))

    def test_should_sum_distance_example_1(self):
        # GIVEN
        state = TestAmphipod._parse_input(
            lines="""#############
#...C...B...#
###B#.#.#D###
  #A#D#C#A#
  #########
""".splitlines(keepends=True)
        )

        # WHEN
        res = _sum_distances(state)

        # THEN
        assert_that(res, equal_to(7489))

    def test_should_sum_distance_example_2(self):
        # GIVEN
        state = TestAmphipod._parse_input(
            lines="""#############
#.....C.B...#
###B#.#.#D###
  #A#D#C#A#
  #########
""".splitlines(keepends=True)
        )

        # WHEN
        res = _sum_distances(state)

        # THEN
        assert_that(res, equal_to(7289))

    def test_should_organize_for_intermediate_state_example_1(self):
        # GIVEN
        state = TestAmphipod._parse_input(
            lines="""#############
#.......B...#
###B#C#.#D###
  #A#D#C#A#
  #########
""".splitlines(keepends=True)
        )

        done_state = TestAmphipod._parse_input(
            lines="""#############
#.......B...#
###B#.#C#D###
  #A#D#C#A#
  #########
""".splitlines(keepends=True)
)

        # WHEN
        res = organize(state, done_state=done_state)

        # THEN
        assert_that(res, equal_to(400))

    @pytest.mark.slow
    def test_should_organize_for_given_example(self):
        # GIVEN
        state = TestAmphipod._given_sample()

        # WHEN
        res = organize(state)

        # THEN
        assert_that(res, equal_to(12521))

    @pytest.mark.slow
    def test_should_organize_for_given_input(self):
        # GIVEN
        state = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestAmphipod._parse_input
        )

        # WHEN
        res = organize(state)

        # THEN
        assert_that(res, equal_to(14467))
