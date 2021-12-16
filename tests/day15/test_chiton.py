from typing import Iterable, List

import pytest
from hamcrest import assert_that, equal_to

from aoc.day15.chiton import shorted_path, get_matrix_weight, Coordinate
from aoc.util.input import parse_input_file
from aoc.util.matrix import initialize_matrix


class TestChiton:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> List[List[int]]:
        return [
            TestChiton._parse_line(line.strip())
            for line in lines
        ]

    @staticmethod
    def _parse_line(line: str) -> List[int]:
        return list(map(int, line))

    def test_should_analyze_shortest_path_for_given_sample(self):
        # GIVEN
        matrix = TestChiton._parse_input(
            lines="""1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""".splitlines(keepends=True)
        )

        # WHEN
        res = shorted_path(matrix)

        # THEN
        assert_that(res, equal_to(40))

    def test_should_analyze_shortest_path_for_small_sample(self):
        # GIVEN
        matrix = TestChiton._parse_input(
            lines="""931
678
419
""".splitlines(keepends=True)
        )

        # WHEN
        res = shorted_path(matrix)

        # THEN
        assert_that(res, equal_to(20))

    def test_should_go_up_if_needed(self):
        # GIVEN
        matrix = TestChiton._parse_input(
            lines="""19111
11191
99991
99991
""".splitlines(keepends=True)
        )

        # WHEN
        res = shorted_path(matrix)

        # THEN
        assert_that(res, equal_to(9))

    def test_should_analyze_shortest_path_for_input(self):
        # GIVEN
        matrix = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestChiton._parse_input
        )

        # WHEN
        res = shorted_path(matrix)

        # THEN
        assert_that(res, equal_to(698))

    def test_should_analyze_shortest_path_for_given_sample_part2(self):
        # GIVEN
        matrix = TestChiton._parse_input(
            lines="""1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""".splitlines(keepends=True)
        )

        # WHEN
        res = shorted_path(matrix, ratio=5)

        # THEN
        assert_that(res, equal_to(315))

    @pytest.mark.slow
    def test_should_analyze_shortest_path_for_input_part2(self):
        # GIVEN
        matrix = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestChiton._parse_input
        )

        # WHEN
        res = shorted_path(matrix, ratio=5)

        # THEN
        assert_that(res, equal_to(3022))

    def test_should_translate_weight(self):
        # GIVEN
        matrix = [[8]]

        # WHEN
        translated_matrix = initialize_matrix(-1, 5, 5)
        for y in range(5):
            for x in range(5):
                translated_matrix[y][x] = get_matrix_weight(Coordinate(x, y), matrix)

        # THEN
        assert_that(translated_matrix, equal_to([
            [8, 9, 1, 2, 3],
            [9, 1, 2, 3, 4],
            [1, 2, 3, 4, 5],
            [2, 3, 4, 5, 6],
            [3, 4, 5, 6, 7]
        ]))
