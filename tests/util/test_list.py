from hamcrest import assert_that, equal_to

from aoc.util.list import flat_map


class TestFlatMap:
    def test_should_flatten_a_list_of_list(self):
        # GIVEN
        li = [[1, 2, 3], [4, 5]]

        # WHEN
        res = flat_map(li)

        # THEN
        assert_that(res, equal_to([1, 2, 3, 4, 5]))
