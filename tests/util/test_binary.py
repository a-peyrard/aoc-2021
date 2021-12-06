from hamcrest import assert_that, equal_to

from aoc.util.binary import get_bit_at, turn_on_bit_at


class TestGetBitAt:
    def test_should_get_bit_at_specified_index(self):
        # GIVEN
        num = int('1011', 2)

        # WHEN
        bit0 = get_bit_at(num, 0)
        bit1 = get_bit_at(num, 1)
        bit2 = get_bit_at(num, 2)
        bit3 = get_bit_at(num, 3)

        # THEN
        assert_that(bit0, equal_to(1))
        assert_that(bit1, equal_to(1))
        assert_that(bit2, equal_to(0))
        assert_that(bit3, equal_to(1))


class TestTurnOnBitAt:
    def test_should_change_bit_value(self):
        # GIVEN
        num = 0

        # WHEN
        num = turn_on_bit_at(num, 0)
        num = turn_on_bit_at(num, 1)
        num = turn_on_bit_at(num, 3)

        # THEN
        assert_that(num, equal_to(11))
