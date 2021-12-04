from hamcrest import assert_that, equal_to

from aoc.util.num import binary_to_string


class TestBinaryToString:
    def test_should_print_binary(self):
        # GIVEN
        a = 9

        # WHEN
        res = binary_to_string(a, 10)

        # THEN
        assert_that(res, equal_to("0000001001"))
