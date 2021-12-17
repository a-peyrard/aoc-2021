from typing import Iterable, Tuple

from hamcrest import assert_that, equal_to

from aoc.day17.trick_shot import launch_probe, count_number_of_solutions, simulate_launch
from aoc.util.input import parse_input_file


class TestTrickShot:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> Tuple[int, int, int, int]:
        first_line = next(lines.__iter__()).strip()
        raw_x, raw_y = first_line[13:].split(", ")
        x_min, x_max = raw_x[2:].split("..")
        y_min, y_max = raw_y[2:].split("..")
        return int(x_min), int(x_max), int(y_min), int(y_max)

    def test_should_launch_probe_for_given_sample(self):
        # GIVEN
        target = TestTrickShot._parse_input(
            lines="""target area: x=20..30, y=-10..-5
""".splitlines(keepends=True)
        )

        # WHEN
        res = launch_probe(target)

        # THEN
        assert_that(res, equal_to(45))

    def test_should_launch_probe_for_input(self):
        # GIVEN
        target = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestTrickShot._parse_input
        )

        # WHEN
        res = launch_probe(target)

        # THEN
        assert_that(res, equal_to(13203))

    def test_should_count_number_of_solutions_for_given_sample(self):
        # GIVEN
        target = TestTrickShot._parse_input(
            lines="""target area: x=20..30, y=-10..-5
""".splitlines(keepends=True)
        )

        # WHEN
        res = count_number_of_solutions(target)

        # THEN
        assert_that(res, equal_to(112))

    def test_should_count_number_of_solutions_for_input(self):
        # GIVEN
        target = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestTrickShot._parse_input
        )

        # WHEN
        res = count_number_of_solutions(target)

        # THEN
        assert_that(res, equal_to(5644))

    def test_should_simulate_launch_for_example_1_in_sample(self):
        # GIVEN
        target = TestTrickShot._parse_input(
            lines="""target area: x=20..30, y=-10..-5
""".splitlines(keepends=True)
        )

        # WHEN
        res = simulate_launch((7, 2), target)

        # THEN
        assert_that(res, equal_to(True))

    def test_should_simulate_launch_for_example_2_in_sample(self):
        # GIVEN
        target = TestTrickShot._parse_input(
            lines="""target area: x=20..30, y=-10..-5
""".splitlines(keepends=True)
        )

        # WHEN
        res = simulate_launch((6, 3), target)

        # THEN
        assert_that(res, equal_to(True))

    def test_should_simulate_launch_for_example_3_in_sample(self):
        # GIVEN
        target = TestTrickShot._parse_input(
            lines="""target area: x=20..30, y=-10..-5
""".splitlines(keepends=True)
        )

        # WHEN
        res = simulate_launch((6, 9), target)

        # THEN
        assert_that(res, equal_to(True))

    def test_should_simulate_launch_for_example_4_in_sample(self):
        # GIVEN
        target = TestTrickShot._parse_input(
            lines="""target area: x=20..30, y=-10..-5
""".splitlines(keepends=True)
        )

        # WHEN
        res = simulate_launch((9, 0), target)

        # THEN
        assert_that(res, equal_to(True))

    def test_should_simulate_launch_for_example_5_in_sample(self):
        # GIVEN
        target = TestTrickShot._parse_input(
            lines="""target area: x=20..30, y=-10..-5
""".splitlines(keepends=True)
        )

        # WHEN
        res = simulate_launch((17, -4), target)

        # THEN
        assert_that(res, equal_to(False))

    def test_should_simulate_launches_for_input(self):
        # GIVEN
        target = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestTrickShot._parse_input
        )
        simulations = [
            (125, -163)
        ]

        # WHEN
        for simulation in simulations:
            simulate_launch(simulation, target, generate_image=True)

        # THEN
        assert_that(1, equal_to(1))
