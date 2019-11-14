import numpy as np
import pytest

from optimal_mapping.analyzer import RouteAnalyzer


@pytest.fixture
def matrix():
    return [
        [14, 12, 15, 15],
        [21, 18, 18, 22],
        [14, 17, 12, 14],
        [6, 5, 3, 6],
    ]


def test_total_zero_values():
    matrix = np.array([[2, 4, 7, 2, 0], [0, 9, 7, 5, 4], [6, 7, 0, 0, 2], [2, 0, 1, 1, 0], [0, 5, 7, 1, 7]])

    analyzer = RouteAnalyzer(matrix)

    assert analyzer.total_zero_values == 7


def test_rows_reductions(matrix):
    expected_result = np.array([[2, 0, 3, 3], [3, 0, 0, 4], [2, 5, 0, 2], [3, 2, 0, 3]])
    analyzer = RouteAnalyzer(matrix)
    analyzer._rows_reductions()

    assert np.array_equal(analyzer.matrix, expected_result)


def test_columns_subtraction(matrix):
    expected_result = np.array([[8, 7, 12, 9], [15, 13, 15, 16], [8, 12, 9, 8], [0, 0, 0, 0]])
    analyzer = RouteAnalyzer(matrix)
    analyzer._columns_reductions()

    assert np.array_equal(analyzer.matrix, expected_result)


def test_rows_scanning_doesnt_add_vertical_lines_if_zero_is_not_found():
    matrix = np.array([[2, 4], [1, 9]])
    analyzer = RouteAnalyzer(matrix)
    analyzer._rows_scanning()

    assert analyzer._vertical_lines == []


def test_rows_scanning_doesnt_add_vertical_lines_if_finds_more_than_one_zero():
    matrix = np.array([[2, 0, 4, 0, 1], [0, 1, 9, 0, 0]])
    analyzer = RouteAnalyzer(matrix)
    analyzer._rows_scanning()

    assert analyzer._vertical_lines == []


def test_rows_scanning():
    matrix = np.array([[2, 4, 7, 2, 0], [0, 9, 7, 5, 4], [6, 7, 0, 0, 2], [2, 0, 1, 1, 0], [0, 5, 7, 1, 7]])
    analyzer = RouteAnalyzer(matrix)
    analyzer._rows_scanning()

    assert analyzer._chosen_zeros == [(0, 4), (1, 0), (3, 1)]
    assert sorted(analyzer._vertical_lines) == [0, 1, 4]
    assert analyzer._zeros_scratched == {(0, 4), (3, 4), (1, 0), (4, 0), (3, 1)}


def test_columns_scanning_doesnt_cadd_horizontal_lines_if_zero_is_not_found():
    matrix = np.array([[2, 4], [1, 9]])
    analyzer = RouteAnalyzer(matrix)
    analyzer._columns_scanning()

    assert analyzer._horizontal_lines == []


def test_columns_scanning_doesnt_add_horizontal_lines_if_finds_more_than_one_zero():
    matrix = np.array([[2, 4, 0, 1], [1, 9, 5, 0], [7, 1, 0, 0], [2, 1, 9, 0]])
    analyzer = RouteAnalyzer(matrix)
    analyzer._columns_scanning()

    assert analyzer._horizontal_lines == []


def test_columns_scanning():
    matrix = np.array([
        [2, 4, 7, 2, 0],
        [0, 9, 7, 5, 4],
        [6, 7, 0, 0, 2],
        [2, 0, 1, 1, 0],
        [0, 5, 7, 1, 7]
    ])

    analyzer = RouteAnalyzer(matrix)
    analyzer._columns_scanning()

    assert analyzer._chosen_zeros == [(3, 1), (2, 2), (0, 4)]
    assert sorted(analyzer._horizontal_lines) == [0, 2, 3]
    assert analyzer._zeros_scratched == {(3, 1), (3, 4), (2, 2), (2, 3), (0, 4)}



def test_matrix_scanning():
    matrix = np.array(
        [
            [2, 4, 7, 2, 0],
            [0, 9, 7, 5, 4],
            [6, 7, 0, 0, 2],
            [2, 0, 1, 1, 0],
            [0, 5, 7, 1, 7]
        ]
    )

    analyzer = RouteAnalyzer(matrix)
    analyzer.matrix_scanning()

    assert analyzer._chosen_zeros == [(0, 4), (1, 0), (3, 1), (2, 2)]
    assert sorted(analyzer._vertical_lines) == [0, 1, 4]
    assert sorted(analyzer._horizontal_lines) == [2]
    assert analyzer._zeros_scratched == {(0, 4), (1, 0), (2, 2), (2, 3), (3, 1), (3, 4), (4, 0)}


def test_matrix_scanning_does_more_than_one_loop():
    matrix = np.array(
        [
            [0, 0, 3, 1],
            [1, 0, 0, 2],
            [0, 5, 0, 0],
            [1, 2, 0, 1]
        ]
    )

    analyzer = RouteAnalyzer(matrix)
    analyzer.matrix_scanning()

    assert analyzer._chosen_zeros == [(3, 2),  (2, 3), (1, 1), (0, 0)]
    assert sorted(analyzer._vertical_lines) == [1, 2]
    assert sorted(analyzer._horizontal_lines) == [0, 2]
    assert analyzer._zeros_scratched == {(3, 2),  (2, 3), (1, 1), (0, 0), (2, 2), (2, 0), (1, 2), (0, 1)}


def test_reset_scanning_values(matrix):
    analyzer = RouteAnalyzer(matrix)
    analyzer._chosen_zeros = [1,2,3]
    analyzer._vertical_lines = [1,2,3]
    analyzer._horizontal_lines = [1,2,3]
    analyzer._zeros_scratched = {1,2,3}

    analyzer._reset_scanning_values()

    assert analyzer._chosen_zeros == list()
    assert analyzer._vertical_lines == list()
    assert analyzer._horizontal_lines == list()
    assert analyzer._zeros_scratched == set()


def test_matrix_reduction(matrix):
    expected_matrix = np.array(
        [
            [0, 0, 3, 1],
            [1, 0, 0, 2],
            [0, 5, 0, 0],
            [1, 2, 0, 1]
        ]
    )
    analyzer = RouteAnalyzer(matrix)
    analyzer.matrix_reduction()

    assert np.array_equal(analyzer.matrix, expected_matrix)


def test_get_intersection_points(matrix):
    analyzer = RouteAnalyzer(matrix)
    analyzer._vertical_lines = {0, 1, 4}
    analyzer._horizontal_lines = {2}
    result = [x for x in analyzer._get_intersection_points()]

    assert result == [(2, 0), (2, 1), (2, 4)]


def test_sum_value_at_intersection_points_cells():
    matrix = np.array(
        [
            [2, 4, 7, 2, 0],
            [0, 9, 7, 5, 4],
            [6, 7, 0, 0, 2],
            [2, 0, 1, 1, 0],
            [0, 5, 7, 1, 7]
        ]
    )
    expected_matrix = np.array(
        [
            [2, 4, 7, 2, 0],
            [0, 9, 7, 5, 4],
            [7, 8, 0, 0, 3],
            [2, 0, 1, 1, 0],
            [0, 5, 7, 1, 7]
        ]
    )

    analyzer = RouteAnalyzer(matrix)
    analyzer._vertical_lines = {0, 1, 4}
    analyzer._horizontal_lines = {2}
    analyzer._sum_value_at_intersection_points_cells(1)

    assert np.array_equal(analyzer.matrix, expected_matrix)


def test_get_undeleted_cells():
    matrix = np.array(
        [
            [2, 4, 7, 2, 0],
            [0, 9, 7, 5, 4],
            [6, 7, 0, 0, 2],
            [2, 0, 1, 1, 0],
            [0, 5, 7, 1, 7]
        ]
    )
    analyzer = RouteAnalyzer(matrix)
    analyzer._vertical_lines = {0, 1, 4}
    analyzer._horizontal_lines = {2}
    result = [x for x in analyzer._get_undeleted_cells()]

    assert result == [(0, 2), (0, 3), (1, 2), (1, 3), (3, 2), (3, 3), (4, 2), (4, 3)]


def test_get_min_value_from_undeleted_cells():
    matrix = np.array(
        [
            [2, 4, 7, 2, 0],
            [0, 9, 7, 5, 4],
            [6, 7, 0, 0, 2],
            [2, 0, 1, 1, 0],
            [0, 5, 7, 1, 7]
        ]
    )
    analyzer = RouteAnalyzer(matrix)
    analyzer._vertical_lines = {0, 1, 4}
    analyzer._horizontal_lines = {2}
    result = analyzer._get_min_value_from_undeleted_cells()

    assert result == 1


def test_subtract_value_from_undeleted_cells():
    matrix = np.array(
        [
            [2, 4, 7, 2, 0],
            [0, 9, 7, 5, 4],
            [6, 7, 0, 0, 2],
            [2, 0, 1, 1, 0],
            [0, 5, 7, 1, 7]
        ]
    )
    expected_matrix = np.array(
        [
            [2, 4, 6, 1, 0],
            [0, 9, 6, 4, 4],
            [6, 7, 0, 0, 2],
            [2, 0, 0, 0, 0],
            [0, 5, 6, 0, 7]
        ]
    )
    analyzer = RouteAnalyzer(matrix)
    analyzer._vertical_lines = {0, 1, 4}
    analyzer._horizontal_lines = {2}
    analyzer._subtract_value_from_undeleted_cells(1)

    assert np.array_equal(analyzer.matrix, expected_matrix)


def test_run_with_simple_case(matrix):
    analyzer = RouteAnalyzer(matrix)
    result = analyzer.run()

    assert result == [(3, 2),  (2, 3), (1, 1), (0, 0)]


def test_run_with_complex_test_case():
    matrix = np.array(
        [
            [9, 11, 14, 11, 7],
            [6, 15, 13, 13, 10],
            [12, 13, 6, 8, 8],
            [11, 9, 10, 12, 9],
            [7, 12, 14, 10, 14],
        ]
    )
    analyzer = RouteAnalyzer(matrix)
    result = analyzer.run()

    assert result == [(0, 4), (1, 0), (4, 3), (3, 1), (2, 2)]


def test_get_stabilized_matrix_with_one_missing_row():
    matrix = np.array(
        [
            [2, 4, 7, 2, 0],
            [0, 9, 7, 5, 4],
            [6, 7, 0, 0, 2],
            [2, 0, 1, 1, 0],
        ]
    )
    expected_matrix = np.array(
        [
            [2, 4, 7, 2, 0],
            [0, 9, 7, 5, 4],
            [6, 7, 0, 0, 2],
            [2, 0, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]
    )
    analyzer = RouteAnalyzer(matrix)

    assert np.array_equal(analyzer.matrix, expected_matrix)


def test_get_stabilized_matrix_with_two_missing_rows():
    matrix = np.array(
        [
            [2, 4, 7, 2, 0],
            [0, 9, 7, 5, 4],
            [6, 7, 0, 0, 2],
        ]
    )
    expected_matrix = np.array(
        [
            [2, 4, 7, 2, 0],
            [0, 9, 7, 5, 4],
            [6, 7, 0, 0, 2],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
    )
    analyzer = RouteAnalyzer(matrix)

    assert np.array_equal(analyzer.matrix, expected_matrix)


def test_get_stabilized_matrix_with_one_missing_column():
    matrix = np.array(
        [
            [2, 4, 7, 2],
            [0, 9, 7, 5],
            [6, 7, 0, 0],
            [2, 0, 1, 1],
            [0, 5, 7, 1]
        ]
    )
    expected_matrix = np.array(
        [
            [2, 4, 7, 2, 0],
            [0, 9, 7, 5, 0],
            [6, 7, 0, 0, 0],
            [2, 0, 1, 1, 0],
            [0, 5, 7, 1, 0]
        ]
    )
    analyzer = RouteAnalyzer(matrix)

    assert np.array_equal(analyzer.matrix, expected_matrix)


def test_get_stabilized_matrix_with_two_missing_columns():
    matrix = np.array(
        [
            [2, 4, 7],
            [0, 9, 7],
            [6, 7, 0],
            [2, 0, 1],
            [0, 5, 7]
        ]
    )
    expected_matrix = np.array(
        [
            [2, 4, 7, 0, 0],
            [0, 9, 7, 0, 0],
            [6, 7, 0, 0, 0],
            [2, 0, 1, 0, 0],
            [0, 5, 7, 0, 0]
        ]
    )
    analyzer = RouteAnalyzer(matrix)

    assert np.array_equal(analyzer.matrix, expected_matrix)