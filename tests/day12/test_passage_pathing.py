from typing import Iterable, List, Tuple

import pytest
from hamcrest import assert_that, equal_to

from aoc.day12.passage_pathing import count_paths
from aoc.util.input import parse_input_file


class TestDumboOctopus:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> List[Tuple[str, str]]:
        return [
            TestDumboOctopus._parse_line(line)
            for line in lines
        ]

    @staticmethod
    def _parse_line(line: str) -> Tuple[str, str]:
        tokens = line.strip().split("-")
        return tokens[0], tokens[1]

    def test_should_count_paths_for_first_given_sample(self):
        # GIVEN
        edges = TestDumboOctopus._parse_input(
            lines="""start-A
start-b
A-c
A-b
b-d
A-end
b-end""".splitlines(keepends=True)
        )

        # WHEN
        res = count_paths(edges)

        # THEN
        assert_that(res, equal_to(10))

    def test_should_count_paths_for_second_given_sample(self):
        # GIVEN
        edges = TestDumboOctopus._parse_input(
            lines="""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""".splitlines(keepends=True)
        )

        # WHEN
        res = count_paths(edges)

        # THEN
        assert_that(res, equal_to(19))

    def test_should_count_paths_for_third_given_sample(self):
        # GIVEN
        edges = TestDumboOctopus._parse_input(
            lines="""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""".splitlines(keepends=True)
        )

        # WHEN
        res = count_paths(edges)

        # THEN
        assert_that(res, equal_to(226))

    def test_should_count_paths_for_input(self):
        # GIVEN
        edges = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestDumboOctopus._parse_input
        )

        # WHEN
        res = count_paths(edges)

        # THEN
        assert_that(res, equal_to(3485))

    def test_should_count_paths_with_joker_for_first_given_sample(self):
        # GIVEN
        edges = TestDumboOctopus._parse_input(
            lines="""start-A
start-b
A-c
A-b
b-d
A-end
b-end""".splitlines(keepends=True)
        )

        # WHEN
        res = count_paths(edges, joker=True)

        # THEN
        assert_that(res, equal_to(36))

    def test_should_count_paths_with_joker_for_second_given_sample(self):
        # GIVEN
        edges = TestDumboOctopus._parse_input(
            lines="""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""".splitlines(keepends=True)
        )

        # WHEN
        res = count_paths(edges, joker=True)

        # THEN
        assert_that(res, equal_to(103))

    def test_should_count_paths_with_joker_for_third_given_sample(self):
        # GIVEN
        edges = TestDumboOctopus._parse_input(
            lines="""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""".splitlines(keepends=True)
        )

        # WHEN
        res = count_paths(edges, joker=True)

        # THEN
        assert_that(res, equal_to(3509))

    @pytest.mark.slow
    def test_should_count_paths_with_joker_for_input(self):
        # GIVEN
        edges = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestDumboOctopus._parse_input
        )

        # WHEN
        res = count_paths(edges, joker=True)

        # THEN
        assert_that(res, equal_to(85062))
