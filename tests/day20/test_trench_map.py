from typing import Iterable, List, Tuple, Set

import pytest
from hamcrest import assert_that, equal_to

from aoc.day20.trench_map import enhance_image, is_a_new_light_pixel, draw_image, count_pixels
from aoc.util.input import parse_input_file


class TestTrenchMap:
    @staticmethod
    def _given_sample() -> Tuple[List[bool], Set[Tuple[int, int]], int, int, int, int]:
        return TestTrenchMap._parse_input(
            lines="""..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""".splitlines(keepends=True)
        )

    @staticmethod
    def _parse_input(lines: Iterable[str]) -> Tuple[List[bool], Set[Tuple[int, int]], int, int, int, int]:
        lines_li = list(lines)
        algo, parsed_lines = TestTrenchMap._parse_algo(lines_li)
        image, x_min, width, y_min, height = TestTrenchMap._parse_image(list(lines_li[parsed_lines + 1:]))
        return algo, image, x_min, width, y_min, height

    @staticmethod
    def _parse_algo(lines: List[str]) -> Tuple[List[bool], int]:
        algo_str = ""
        line_idx = 0
        for raw_line in lines:
            line = raw_line.strip()
            if line:
                algo_str += line
            else:
                break

            line_idx += 1

        return list(map(lambda c: c == "#", algo_str)), line_idx

    @staticmethod
    def _parse_image(lines: List[str]) -> Tuple[Set[Tuple[int, int]], int, int, int, int]:
        image = set()
        y = 0
        for line in lines:
            for x, char in enumerate(line):
                if char == "#":
                    image.add((x, y))
            y += 1

        return image, 0, len(lines[0]) - 1, 0, y

    def test_should_draw_initial_image_from_given_sample(self):
        # GIVEN
        algo, image, x_min, width, y_min, height = TestTrenchMap._given_sample()

        # WHEN
        res = draw_image(image, x_min, width, y_min, height)

        # THEN
        assert_that(
            res,
            equal_to("""#..#.
#....
##..#
..#..
..###
""")
        )

    def test_should_draw_image_for_first_step_in_given_sample(self):
        # GIVEN
        algo, image, x_min, width, y_min, height = TestTrenchMap._given_sample()

        # WHEN
        image_str = draw_image(
            *enhance_image(algo, image, x_min, width, y_min, height, number_of_steps=1)
        )

        # THEN
        assert_that(
            image_str,
            equal_to(""".##.##.
#..#.#.
##.#..#
####..#
.#..##.
..##..#
...#.#.
"""))

    def test_should_count_light_pixel_for_first_step_in_given_sample(self):
        # GIVEN
        algo, image, x_min, width, y_min, height = TestTrenchMap._given_sample()

        # WHEN
        res = count_pixels(algo, image, x_min, width, y_min, height, number_of_steps=1)

        # THEN
        assert_that(res, equal_to(24))

    def test_should_count_light_pixel_for_given_sample(self):
        # GIVEN
        algo, image, x_min, width, y_min, height = TestTrenchMap._given_sample()

        # WHEN
        res = count_pixels(algo, image, x_min, width, y_min, height, number_of_steps=2)

        # THEN
        assert_that(res, equal_to(35))

    @pytest.mark.slow
    def test_should_count_light_pixel_for_given_sample_and_50_steps(self):
        # GIVEN
        algo, image, x_min, width, y_min, height = TestTrenchMap._given_sample()

        # WHEN
        res = count_pixels(algo, image, x_min, width, y_min, height, number_of_steps=50)

        # THEN
        assert_that(res, equal_to(3351))

    def test_should_count_light_pixel_for_given_input(self):
        # GIVEN
        algo, image, x_min, width, y_min, height = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestTrenchMap._parse_input
        )

        # WHEN
        res = count_pixels(algo, image, x_min, width, y_min, height, number_of_steps=2)

        # THEN
        assert_that(res, equal_to(5765))

    @pytest.mark.slow
    def test_should_count_light_pixel_for_given_input_after_50_steps(self):
        # GIVEN
        algo, image, x_min, width, y_min, height = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestTrenchMap._parse_input
        )

        # WHEN
        res = count_pixels(algo, image, x_min, width, y_min, height, number_of_steps=50)

        # THEN
        assert_that(res, equal_to(18509))

    def test_should_count_light_pixel_for_given_input_after_1_step(self):
        # GIVEN
        algo, image, x_min, width, y_min, height = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestTrenchMap._parse_input
        )

        # WHEN
        res = count_pixels(algo, image, x_min, width, y_min, height, number_of_steps=1)

        # THEN
        assert_that(res, equal_to(5616))

    def test_should_check_pixel_is_a_light_pixel_example_1(self):
        # GIVEN
        algo, image, x_min, width, y_min, height = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestTrenchMap._parse_input
        )

        # WHEN
        light = is_a_new_light_pixel(19, -1, algo, image, x_min, width, y_min, height, False)

        # THEN
        assert_that(light, equal_to(False))
