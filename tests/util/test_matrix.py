from hamcrest import assert_that, equal_to

from aoc.util.matrix import initialize_matrix


class TestInitializeMatrix:
    def test_should_initialize_a_matrix(self):
        # GIVEN
        col = 4
        row = 5
        fill = 0

        # WHEN
        matrix = initialize_matrix(fill, row, col)

        # THEN
        assert_that(
            matrix,
            equal_to([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ])
        )

    def test_should_initialize_square_matrix_with_2_params(self):
        # GIVEN
        size = 4
        fill = 0

        # WHEN
        matrix = initialize_matrix(fill, size)

        # THEN
        assert_that(
            matrix,
            equal_to([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ])
        )
