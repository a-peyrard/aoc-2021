from hamcrest import assert_that, equal_to

from aoc.util.circular_buffer import CircularBuffer


class TestCircularBuffer:
    def test_should_push_element_and_return_previous(self):
        # GIVEN
        buffer = CircularBuffer(length=3, initial=[0, 1, 2])

        # WHEN
        push3 = buffer.push(3)
        push4 = buffer.push(4)
        push5 = buffer.push(5)
        push6 = buffer.push(6)
        push7 = buffer.push(7)

        # THEN
        assert_that(push3, equal_to(0))
        assert_that(push4, equal_to(1))
        assert_that(push5, equal_to(2))
        assert_that(push6, equal_to(3))
        assert_that(push7, equal_to(4))
