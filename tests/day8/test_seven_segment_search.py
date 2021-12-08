from typing import Iterable, List, Tuple

from hamcrest import assert_that, equal_to

from aoc.day8.seven_segment_search import count_digit_part1
from aoc.util.input import parse_input_file


class TestCountDigit:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> List[Tuple[List[str], List[str]]]:
        return [
            TestCountDigit._parse_line(line)
            for line in lines
        ]

    @staticmethod
    def _parse_line(line: str) -> Tuple[List[str], List[str]]:
        tokens = line.split(' | ')
        return tokens[0].split(), tokens[1].split()

    def test_should_validate_given_sample(self):
        # GIVEN
        signals = TestCountDigit._parse_input(
            lines="""be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""".splitlines(keepends=True)
        )

        # WHEN
        res = count_digit_part1(signals)

        # THEN
        assert_that(res, equal_to(26))

    def test_should_count_1_4_7_8_for_input(self):
        # GIVEN
        signals = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestCountDigit._parse_input
        )

        # WHEN
        res = count_digit_part1(signals)

        # THEN
        assert_that(res, equal_to(534))
