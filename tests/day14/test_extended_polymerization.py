from typing import Iterable, List, Tuple, Dict

import pytest
from hamcrest import assert_that, equal_to

from aoc.day12.passage_pathing import count_paths
from aoc.day14.extended_polymerization import generate_template
from aoc.util.input import parse_input_file


class TestExtendedPolymerization:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> Tuple[str, Dict[str, str]]:
        lines_li = list(lines)

        template = lines_li[0].strip()
        rules = {}
        for line in lines[2:]:
            from_str, add_char = line.strip().split(" -> ")
            rules[from_str] = add_char

        return template, rules

    def test_should_generate_template_for_given_sample(self):
        # GIVEN
        template, rules = TestExtendedPolymerization._parse_input(
            lines="""NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""".splitlines(keepends=True)
        )

        # WHEN
        res = generate_template(template, rules, nb_steps=10)

        # THEN
        assert_that(res, equal_to(1588))

    def test_should_test_should_generate_template_for_for_input(self):
        # GIVEN
        template, rules = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestExtendedPolymerization._parse_input
        )

        # WHEN
        res = generate_template(template, rules, nb_steps=10)

        # THEN
        assert_that(res, equal_to(2112))
