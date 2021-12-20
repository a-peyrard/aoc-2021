from typing import Iterable, List

import pytest
from hamcrest import assert_that, equal_to, instance_of

from aoc.day18.snailfish import parse, PairNode, ValueNode, sum_numbers, reduce_number, _explode, _split, \
    sum_number_list, do_homework
from aoc.util.input import parse_input_file


class TestSnailfish:
    @staticmethod
    def _parse_input(lines: Iterable[str]) -> List[str]:
        return [line.strip() for line in lines]

    # noinspection PyTypeChecker
    # noinspection PyUnresolvedReferences
    def test_should_parse_basic_pair(self):
        # GIVEN
        number = "[6,1]"

        # WHEN
        res = parse(number)

        # THEN
        assert_that(res.left, instance_of(ValueNode))
        assert_that(res.left.value, equal_to(6))
        assert_that(res.right, instance_of(ValueNode))
        assert_that(res.right  .value, equal_to(1))

    # noinspection PyTypeChecker
    # noinspection PyUnresolvedReferences
    def test_should_parse_nested_pair(self):
        # GIVEN
        number = "[[1,2],6]"

        # WHEN
        res = parse(number)

        # THEN
        assert_that(res.left, instance_of(PairNode))
        assert_that(res.left.left.value, equal_to(1))
        assert_that(res.left.right.value, equal_to(2))
        assert_that(res.right, instance_of(ValueNode))
        assert_that(res.right.value, equal_to(6))

    # noinspection PyTypeChecker
    # noinspection PyUnresolvedReferences
    def test_should_parse_complex_number(self):
        # GIVEN
        number = "[[[1,[8,5]],[[3,9],0]],2]"

        # WHEN
        res = parse(number)

        # THEN
        assert_that(res.left, instance_of(PairNode))
        assert_that(res.left.left, instance_of(PairNode))
        assert_that(res.left.left.left, instance_of(ValueNode))
        assert_that(res.left.left.left.value, equal_to(1))
        assert_that(res.left.left.right, instance_of(PairNode))
        assert_that(res.left.left.right.left.value, equal_to(8))
        assert_that(res.left.left.right.right.value, equal_to(5))

        assert_that(res.left.right, instance_of(PairNode))
        assert_that(res.left.right.left, instance_of(PairNode))
        assert_that(res.left.right.left.left.value, equal_to(3))
        assert_that(res.left.right.left.right.value, equal_to(9))
        assert_that(res.left.right.right, instance_of(ValueNode))
        assert_that(res.left.right.right.value, equal_to(0))

        assert_that(res.right, instance_of(ValueNode))
        assert_that(res.right  .value, equal_to(2))

    def test_should_print_complex_number(self):
        # GIVEN
        number = "[[[1,[8,5]],[[3,9],0]],2]"

        # WHEN
        res = parse(number).print()

        # THEN
        assert_that(res, equal_to(number))

    def test_should_sum_numbers_example_1(self):
        # GIVEN
        num1 = "[1,2]"
        num2 = "[[3,4],5]"

        # WHEN
        res = sum_numbers(parse(num1), parse(num2)).print()

        # THEN
        assert_that(res, equal_to("[[1,2],[[3,4],5]]"))

    def test_should_reduce_number_example_1(self):
        # GIVEN
        number = "[[[[[9,8],1],2],3],4]"

        # WHEN
        res = reduce_number(parse(number)).print()

        # THEN
        assert_that(res, equal_to("[[[[0,9],2],3],4]"))

    def test_should_reduce_number_example_2(self):
        # GIVEN
        number = "[7,[6,[5,[4,[3,2]]]]]"

        # WHEN
        res = reduce_number(parse(number)).print()

        # THEN
        assert_that(res, equal_to("[7,[6,[5,[7,0]]]]"))

    def test_should_reduce_number_example_3(self):
        # GIVEN
        number = "[[6,[5,[4,[3,2]]]],1]"

        # WHEN
        res = reduce_number(parse(number)).print()

        # THEN
        assert_that(res, equal_to("[[6,[5,[7,0]]],3]"))

    def test_should_reduce_number_example_4(self):
        # GIVEN
        number = "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"

        # WHEN
        res = reduce_number(parse(number)).print()

        # THEN
        assert_that(res, equal_to("[[3,[2,[8,0]]],[9,[5,[7,0]]]]"))

    def test_should_reduce_number_example_5(self):
        # GIVEN
        number = "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"

        # WHEN
        res = reduce_number(parse(number)).print()

        # THEN
        assert_that(res, equal_to("[[3,[2,[8,0]]],[9,[5,[7,0]]]]"))

    def test_should_reduce_number_example_6(self):
        # GIVEN
        number = "[1,[2,11]]"

        # WHEN
        res = reduce_number(parse(number)).print()

        # THEN
        assert_that(res, equal_to("[1,[2,[5,6]]]"))

    def test_should_explode_number_example_1(self):
        # GIVEN
        number = parse("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]")
        # [,[1,1]]

        # WHEN
        _explode(number)

        # THEN
        assert_that(number.print(), equal_to("[[[[0,7],4],[15,[0,13]]],[1,1]]"))

    def test_should_explode_number_example_2(self):
        # GIVEN
        number = parse("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")
        # [,[1,1]]

        # WHEN
        _explode(number)

        # THEN
        assert_that(number.print(), equal_to("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"))

    def test_should_reduce_number_example_final_step_by_step(self):
        # GIVEN
        number = parse("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")

        # WHENs & THENs

        # after explode:  [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
        _explode(number)
        assert_that(number.print(), equal_to("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"))
        # after explode:  [[[[0,7],4],[15,[0,13]]],[1,1]]
        _explode(number)
        assert_that(number.print(), equal_to("[[[[0,7],4],[15,[0,13]]],[1,1]]"))
        # after split:    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
        _split(number)
        assert_that(number.print(), equal_to("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"))
        # after split:    [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
        _split(number)
        assert_that(number.print(), equal_to("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"))
        # after explode:  [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
        _explode(number)
        assert_that(number.print(), equal_to("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"))

    def test_should_reduce_number_example_final(self):
        # GIVEN
        number = "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"

        # WHEN
        res = reduce_number(parse(number)).print()

        # THEN
        assert_that(res, equal_to("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"))

    def test_should_sum_number_list_example_1(self):
        # GIVEN
        numbers = [
            "[1,1]",
            "[2,2]",
            "[3,3]",
            "[4,4]"
        ]

        # WHEN
        res = sum_number_list(list(map(parse, numbers))).print()

        # THEN
        assert_that(res, equal_to("[[[[1,1],[2,2]],[3,3]],[4,4]]"))

    def test_should_sum_number_list_example_2(self):
        # GIVEN
        numbers = [
            "[1,1]",
            "[2,2]",
            "[3,3]",
            "[4,4]",
            "[5,5]"
        ]

        # WHEN
        res = sum_number_list(list(map(parse, numbers))).print()

        # THEN
        assert_that(res, equal_to("[[[[3,0],[5,3]],[4,4]],[5,5]]"))

    def test_should_sum_number_list_example_3(self):
        # GIVEN
        numbers = [
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
            "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
            "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
            "[7,[5,[[3,8],[1,4]]]]",
            "[[2,[2,2]],[8,[8,1]]]",
            "[2,9]",
            "[1,[[[9,3],9],[[9,0],[0,7]]]]",
            "[[[5,[7,4]],7],1]",
            "[[[[4,2],2],6],[8,7]]",
        ]

        # WHEN
        res = sum_number_list(list(map(parse, numbers))).print()

        # THEN
        assert_that(res, equal_to("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"))

    def test_should_calculate_magnitude_example_1(self):
        # GIVEN
        number = "[9,1]"

        # WHEN
        res = parse(number).magnitude()

        # THEN
        assert_that(res, equal_to(29))

    def test_should_calculate_magnitude_example_2(self):
        # GIVEN
        number = "[1,9]"

        # WHEN
        res = parse(number).magnitude()

        # THEN
        assert_that(res, equal_to(21))

    def test_should_calculate_magnitude_example_3(self):
        # GIVEN
        number = "[[9,1],[1,9]]"

        # WHEN
        res = parse(number).magnitude()

        # THEN
        assert_that(res, equal_to(129))

    def test_should_calculate_some_magnitudes(self):
        # GIVEN
        num1 = "[[1,2],[[3,4],5]]"
        num2 = "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
        num3 = "[[[[1,1],[2,2]],[3,3]],[4,4]]"
        num4 = "[[[[3,0],[5,3]],[4,4]],[5,5]]"
        num5 = "[[[[5,0],[7,4]],[5,5]],[6,6]]"
        num6 = "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"

        # WHEN
        magnitude1 = parse(num1).magnitude()
        magnitude2 = parse(num2).magnitude()
        magnitude3 = parse(num3).magnitude()
        magnitude4 = parse(num4).magnitude()
        magnitude5 = parse(num5).magnitude()
        magnitude6 = parse(num6).magnitude()

        # THEN
        assert_that(magnitude1, equal_to(143))
        assert_that(magnitude2, equal_to(1384))
        assert_that(magnitude3, equal_to(445))
        assert_that(magnitude4, equal_to(791))
        assert_that(magnitude5, equal_to(1137))
        assert_that(magnitude6, equal_to(3488))

    def test_should_do_homework_for_given_sample(self):
        # GIVEN
        numbers = TestSnailfish._parse_input(
            lines="""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""".splitlines(keepends=True)
        )

        # WHEN
        res = do_homework(numbers)

        # THEN
        assert_that(res, equal_to(4140))

    def test_should_do_homework_for_input(self):
        # GIVEN
        numbers = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestSnailfish._parse_input
        )

        # WHEN
        res = do_homework(numbers)

        # THEN
        assert_that(res, equal_to(3981))

    def test_should_explode_for_broken_step(self):
        # GIVEN
        number = parse("[[[[14,15],[7,13]],[[12,6],[0,[12,5]]]],[[[[4,1],[4,1]],[2,[5,5]]],[1,[0,[0,6]]]]]")

        # WHEN
        _explode(number)

        # THEN
        assert_that(
            number.print(),
            equal_to("[[[[14,15],[7,13]],[[12,6],[12,0]]],[[[[9,1],[4,1]],[2,[5,5]]],[1,[0,[0,6]]]]]")
        )

    def test_should_not_reuse_same_tree_for_parse(self):
        # GIVEN
        raw_number = "[[4,1],[4,1]]"

        # WHEN
        number = parse(raw_number)
        # noinspection PyUnresolvedReferences
        number.left.left.value = 5

        # THEN
        assert_that(
            number.print(),
            equal_to("[[5,1],[4,1]]")
        )

    @pytest.mark.slow
    def test_should_get_maximum_magnitude_for_input(self):
        # GIVEN
        numbers = parse_input_file(
            origin=__file__,
            filename='input.txt',
            callback=TestSnailfish._parse_input
        )

        # WHEN
        magnitudes: List[int] = []
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                magnitudes.append(reduce_number(sum_numbers(parse(numbers[i]), parse(numbers[j]))).magnitude())
                magnitudes.append(reduce_number(sum_numbers(parse(numbers[j]), parse(numbers[i]))).magnitude())

        # THEN
        assert_that(max(magnitudes), equal_to(4687))
