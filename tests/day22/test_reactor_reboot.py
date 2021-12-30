from typing import Iterable, Tuple, List

import pytest
from hamcrest import assert_that, equal_to

# noinspection PyProtectedMember
from aoc.day22.reactor_reboot import Range, Instruction, count_cubes, _restrict_instruction
from aoc.util.input import parse_input_file


class TestReactorReboot:
    @staticmethod
    def _given_sample() -> List[Instruction]:
        return TestReactorReboot._parse_input(
            lines="""on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
""".splitlines(keepends=True)
        )

    @staticmethod
    def _parse_input(lines: Iterable[str]) -> List[Instruction]:
        return [
            TestReactorReboot._parse_line(line.strip())
            for line in lines
        ]

    @staticmethod
    def _solution_1_zone() -> Tuple[Range, Range, Range]:
        return Range(-50, 50), Range(-50, 50), Range(-50, 50)

    @staticmethod
    def _parse_line(line: str) -> Instruction:
        on_off, ranges = line.split()
        x, y, z = ranges.split(",")

        return Instruction(
            on_off == "on",
            TestReactorReboot._parse_range(x),
            TestReactorReboot._parse_range(y),
            TestReactorReboot._parse_range(z)
        )

    @staticmethod
    def _parse_range(raw_range: str) -> Range:
        start, end = raw_range[2:].split("..")
        return Range(int(start), int(end))

    def test_should_count_cubes_for_small_example(self):
        # GIVEN
        instructions = TestReactorReboot._parse_input(
            lines="""on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
""".splitlines(keepends=True)
        )

        # WHEN
        res = count_cubes(instructions, TestReactorReboot._solution_1_zone())

        # THEN
        assert_that(res, equal_to(39))

    @pytest.mark.slow
    def test_should_count_cubes_for_given_example(self):
        # GIVEN
        instructions = TestReactorReboot._given_sample()

        # WHEN
        res = count_cubes(instructions, TestReactorReboot._solution_1_zone())

        # THEN
        assert_that(res, equal_to(590784))

    @pytest.mark.slow
    def test_should_compute_solution_1_for_given_input(self):
        # GIVEN
        instructions = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestReactorReboot._parse_input
        )

        # WHEN
        res = count_cubes(instructions, TestReactorReboot._solution_1_zone())

        # THEN
        assert_that(res, equal_to(650099))

    def test_should_restrict_instruction(self):
        # GIVEN
        instruction = Instruction(
            on=True,
            x=Range(-200, 1),
            y=Range(-200, 200),
            z=Range(-1, 200),
        )

        # WHEN
        restricted = _restrict_instruction(
            instruction,
            TestReactorReboot._solution_1_zone()
        )

        # THEN
        assert_that(
            restricted,
            equal_to(
                Instruction(
                    on=True,
                    x=Range(-50, 1),
                    y=Range(-50, 50),
                    z=Range(-1, 50),
                )
            )
        )
