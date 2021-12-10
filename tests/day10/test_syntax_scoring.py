from typing import Iterable, List

from hamcrest import assert_that, equal_to

from aoc.day10.syntax_scoring import calculate_corrupted_score
from aoc.util.input import parse_input_file


class TestSyntaxScoring:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> List[str]:
        return [
            line.strip()
            for line in lines
        ]

    def test_should_validate_given_sample(self):
        # GIVEN
        lines = TestSyntaxScoring._parse_input(
            lines="""[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".splitlines(keepends=True)
        )

        # WHEN
        res = calculate_corrupted_score(lines)

        # THEN
        assert_that(res, equal_to(26397))

    def test_should_count_low_points_for_input(self):
        # GIVEN
        lines = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestSyntaxScoring._parse_input
        )

        # WHEN
        res = calculate_corrupted_score(lines)

        # THEN
        assert_that(res, equal_to(413733))
