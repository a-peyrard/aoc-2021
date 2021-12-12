from typing import Iterable, List

from hamcrest import assert_that, equal_to

from aoc.day11.dumbo_octopus import count_flashes, print_matrix, find_all_octopus_flashes
from aoc.util.input import parse_input_file


class TestDumboOctopus:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> List[List[int]]:
        return [
            [
                int(c)
                for c in line.strip()
            ]
            for line in lines
        ]

    def test_should_count_flashes_for_given_sample_for_2nd_step(self):
        # GIVEN
        matrix = TestDumboOctopus._parse_input(
            lines="""6594254334
3856965822
6375667284
7252447257
7468496589
5278635756
3287952832
7993992245
5957959665
6394862637""".splitlines(keepends=True)
        )

        # WHEN
        res = count_flashes(matrix, nb_steps=1)

        # THEN
        assert_that(res, equal_to(35))

    def test_should_count_flashes_for_given_sample_after_2_steps(self):
        # GIVEN
        matrix = TestDumboOctopus._parse_input(
            lines="""5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".splitlines(keepends=True)
        )

        # WHEN
        res = count_flashes(matrix, nb_steps=2)

        # THEN
        assert_that(res, equal_to(35))

    def test_should_count_flashes_for_given_sample_after_10_steps(self):
        # GIVEN
        matrix = TestDumboOctopus._parse_input(
            lines="""5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".splitlines(keepends=True)
        )

        # WHEN
        res = count_flashes(matrix, nb_steps=10)

        # THEN
        print_matrix(matrix, 10)
        assert_that(res, equal_to(204))

    def test_should_count_flashes_for_given_sample(self):
        # GIVEN
        matrix = TestDumboOctopus._parse_input(
            lines="""5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".splitlines(keepends=True)
        )

        # WHEN
        res = count_flashes(matrix, nb_steps=100)

        # THEN
        assert_that(res, equal_to(1656))

    def test_should_count_flashes_for_small_sample(self):
        # GIVEN
        matrix = TestDumboOctopus._parse_input(
            lines="""11111
19991
19191
19991
11111""".splitlines(keepends=True)
        )

        # WHEN
        res = count_flashes(matrix, nb_steps=1)

        # THEN
        assert_that(res, equal_to(9))

    def test_should_count_flashes_for_input(self):
        # GIVEN
        matrix = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestDumboOctopus._parse_input
        )

        # WHEN
        res = count_flashes(matrix, nb_steps=100)

        # THEN
        assert_that(res, equal_to(1749))

    def test_should_find_all_octopus_flashes_for_given_sample(self):
        # GIVEN
        matrix = TestDumboOctopus._parse_input(
            lines="""5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".splitlines(keepends=True)
        )

        # WHEN
        res = find_all_octopus_flashes(matrix)

        # THEN
        assert_that(res, equal_to(195))

    def test_should_find_all_octopus_flashes_for_input(self):
        # GIVEN
        matrix = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestDumboOctopus._parse_input
        )

        # WHEN
        res = find_all_octopus_flashes(matrix)

        # THEN
        assert_that(res, equal_to(285))
