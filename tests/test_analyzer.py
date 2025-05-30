# python 3.8.0
import numpy as np
import pytest

from optimal_mapping.analyzer import RouteAnalyzer


@pytest.mark.parametrize(
    "matrix, expected_result",
    (
        ([[2, 4, 7, 2, 0], [0, 9, 7, 5, 4], [6, 7, 0, 0, 2], [2, 0, 1, 1, 0], [0, 5, 7, 1, 7]], 7),
        ([[2, 0, 3, 3], [3, 0, 0, 4], [2, 5, 0, 2], [3, 2, 0, 3]], 5),
    ),
)
def test_total_zero_values(matrix, expected_result):
    analyzer = RouteAnalyzer(matrix)
    assert analyzer._total_zero_values == expected_result


@pytest.mark.parametrize(
    "original_matrix, expected_matrix",
    (
        ([[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6], [0, 0, 0]]),
        ([[1, 2, 3, 4], [4, 5, 6, 7]], [[1, 2, 3, 4], [4, 5, 6, 7], [0, 0, 0, 0], [0, 0, 0, 0]]),
    ),
)
def test_get_matrix_with_dummy_rows(original_matrix, expected_matrix):
    analyzer = RouteAnalyzer(original_matrix)
    result = analyzer._get_matrix_with_dummy_rows()

    assert np.array_equal(result, np.array(expected_matrix))


@pytest.mark.parametrize(
    "original_matrix, expected_matrix",
    (
        ([[1, 2], [3, 4], [5, 6]], [[1, 2, 0], [3, 4, 0], [5, 6, 0]]),
        ([[1, 2], [3, 4], [5, 6], [7, 8]], [[1, 2, 0, 0], [3, 4, 0, 0], [5, 6, 0, 0], [7, 8, 0, 0]]),
    ),
)
def test_get_matrix_with_dummy_columns(original_matrix, expected_matrix):
    analyzer = RouteAnalyzer(original_matrix)
    result = analyzer._get_matrix_with_dummy_columns()

    assert np.array_equal(result, np.array(expected_matrix))


@pytest.mark.parametrize(
    "original_matrix, expected_matrix",
    (
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
        ([[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6], [0, 0, 0]]),
        ([[1, 2, 3, 4], [4, 5, 6, 7]], [[1, 2, 3, 4], [4, 5, 6, 7], [0, 0, 0, 0], [0, 0, 0, 0]]),
        ([[1, 2], [3, 4], [5, 6]], [[1, 2, 0], [3, 4, 0], [5, 6, 0]]),
        ([[1, 2], [3, 4], [5, 6], [7, 8]], [[1, 2, 0, 0], [3, 4, 0, 0], [5, 6, 0, 0], [7, 8, 0, 0]]),
    ),
)
def test_balance_matrix(original_matrix, expected_matrix):
    analyzer = RouteAnalyzer(original_matrix)
    analyzer._balance_matrix()
    assert np.array_equal(analyzer._matrix, np.array(expected_matrix))


def test_make_reductions(example_matrix):
    expected_result = [[2, 0, 3, 3], [3, 0, 0, 4], [2, 5, 0, 2], [3, 2, 0, 3]]
    analyzer = RouteAnalyzer(example_matrix)
    analyzer._make_reductions(analyzer._matrix)

    assert np.array_equal(analyzer._matrix, expected_result)


def test_matrix_reduction(example_matrix):
    expected_matrix = [[0, 0, 3, 1], [1, 0, 0, 2], [0, 5, 0, 0], [1, 2, 0, 1]]
    analyzer = RouteAnalyzer(example_matrix)
    analyzer._matrix_reduction()

    assert np.array_equal(analyzer._matrix, expected_matrix)


def test_rows_scanning_when_zero_is_not_found():
    matrix = [[2, 4], [1, 9]]
    analyzer = RouteAnalyzer(matrix)
    result = analyzer._rows_scanning()

    assert result is False
    assert analyzer._vertical_lines == []
    assert analyzer._chosen_cells == []
    assert analyzer._zeros_scratched == set()


def test_rows_scanning_when_finds_more_than_one_zero():
    matrix = [[2, 0, 4, 0, 1], [0, 1, 9, 0, 0]]
    analyzer = RouteAnalyzer(matrix)
    result = analyzer._rows_scanning()

    assert result is False
    assert analyzer._vertical_lines == []
    assert analyzer._chosen_cells == []
    assert analyzer._zeros_scratched == set()


def test_rows_scanning():
    matrix = [[2, 4, 7, 2, 0], [0, 9, 7, 5, 4], [6, 7, 0, 0, 2], [2, 0, 1, 1, 0], [0, 5, 7, 1, 7]]
    analyzer = RouteAnalyzer(matrix)
    result = analyzer._rows_scanning()

    assert result is True
    assert analyzer._chosen_cells == [(0, 4), (1, 0), (3, 1)]
    assert sorted(analyzer._vertical_lines) == [0, 1, 4]
    assert analyzer._zeros_scratched == {(0, 4), (3, 4), (1, 0), (4, 0), (3, 1)}


def test_columns_scanning_when_zero_is_not_found():
    matrix = [[2, 4], [1, 9]]
    analyzer = RouteAnalyzer(matrix)
    result = analyzer._columns_scanning()

    assert result is False
    assert analyzer._horizontal_lines == []
    assert analyzer._chosen_cells == []
    assert analyzer._zeros_scratched == set()


def test_columns_scanning_when_finds_more_than_one_zero():
    matrix = [[2, 4, 0, 1], [1, 9, 5, 0], [7, 1, 0, 0], [2, 1, 9, 0]]
    analyzer = RouteAnalyzer(matrix)
    result = analyzer._columns_scanning()

    assert result is False
    assert analyzer._horizontal_lines == []
    assert analyzer._chosen_cells == []
    assert analyzer._zeros_scratched == set()


def test_columns_scanning():
    matrix = [[2, 4, 7, 2, 0], [0, 9, 7, 5, 4], [6, 7, 0, 0, 2], [2, 0, 1, 1, 0], [0, 5, 7, 1, 7]]

    analyzer = RouteAnalyzer(matrix)
    result = analyzer._columns_scanning()

    assert result is True
    assert analyzer._chosen_cells == [(3, 1), (2, 2), (0, 4)]
    assert sorted(analyzer._horizontal_lines) == [0, 2, 3]
    assert analyzer._zeros_scratched == {(3, 1), (3, 4), (2, 2), (2, 3), (0, 4)}


def test_random_scanning():
    matrix = np.array([[2, 0, 0, 2], [4, 6, 0, 0], [2, 0, 2, 0], [0, 2, 3, 0]])
    analyzer = RouteAnalyzer(matrix)
    analyzer._random_scanning()

    assert analyzer._chosen_cells == [(0, 1)]
    assert analyzer._vertical_lines == [1]
    assert analyzer._horizontal_lines == [0]
    assert analyzer._zeros_scratched == {(0, 1), (2, 1), (0, 2)}


def test_reset_scanning_values(example_matrix):
    analyzer = RouteAnalyzer(example_matrix)
    analyzer._chosen_cells = [1, 2, 3]
    analyzer._vertical_lines = [1, 2, 3]
    analyzer._horizontal_lines = [1, 2, 3]
    analyzer._zeros_scratched = {1, 2, 3}

    analyzer._reset_scanning_values()

    assert analyzer._chosen_cells == list()
    assert analyzer._vertical_lines == list()
    assert analyzer._horizontal_lines == list()
    assert analyzer._zeros_scratched == set()


def test_matrix_scanning():
    matrix = [[2, 4, 7, 2, 0], [0, 9, 7, 5, 4], [6, 7, 0, 0, 2], [2, 0, 1, 1, 0], [0, 5, 7, 1, 7]]

    analyzer = RouteAnalyzer(matrix)
    analyzer._matrix_scanning()

    assert analyzer._chosen_cells == [(0, 4), (1, 0), (3, 1), (2, 2)]
    assert sorted(analyzer._vertical_lines) == [0, 1, 4]
    assert sorted(analyzer._horizontal_lines) == [2]
    assert analyzer._zeros_scratched == {(0, 4), (1, 0), (2, 2), (2, 3), (3, 1), (3, 4), (4, 0)}


def test_matrix_scanning_does_more_than_one_loop():
    matrix = [[0, 0, 3, 1], [1, 0, 0, 2], [0, 5, 0, 0], [1, 2, 0, 1]]

    analyzer = RouteAnalyzer(matrix)
    analyzer._matrix_scanning()

    assert analyzer._chosen_cells == [(3, 2), (2, 3), (1, 1), (0, 0)]
    assert sorted(analyzer._vertical_lines) == [1, 2]
    assert sorted(analyzer._horizontal_lines) == [0, 2]
    assert analyzer._zeros_scratched == {(3, 2), (2, 3), (1, 1), (0, 0), (2, 2), (2, 0), (1, 2), (0, 1)}


def test_matrix_scanning_with_multiple_solutions():
    matrix = [[0, 0, 0, 0], [5, 0, 0, 2], [0, 1, 0, 2], [8, 0, 0, 0]]

    analyzer = RouteAnalyzer(matrix)
    analyzer._matrix_scanning()

    assert analyzer._chosen_cells == [(0, 0), (2, 2), (3, 3), (1, 1)]
    assert sorted(analyzer._vertical_lines) == [0, 1, 2]
    assert sorted(analyzer._horizontal_lines) == [0, 3]
    assert analyzer._zeros_scratched == {
        (3, 1),
        (3, 2),
        (3, 3),
        (0, 1),
        (1, 1),
        (1, 2),
        (0, 2),
        (2, 2),
        (2, 0),
        (0, 0),
        (0, 3),
    }


def test_get_undeleted_cells():
    matrix = [[2, 4, 7, 2, 0], [0, 9, 7, 5, 4], [6, 7, 0, 0, 2], [2, 0, 1, 1, 0], [0, 5, 7, 1, 7]]
    analyzer = RouteAnalyzer(matrix)
    analyzer._vertical_lines = {0, 1, 4}
    analyzer._horizontal_lines = {2}
    result = [x for x in analyzer._get_undeleted_cells()]

    assert result == [(0, 2), (0, 3), (1, 2), (1, 3), (3, 2), (3, 3), (4, 2), (4, 3)]


def test_get_min_value_from_undeleted_cells():
    matrix = [[2, 4, 7, 2, 0], [0, 9, 7, 5, 4], [6, 7, 0, 0, 2], [2, 0, 1, 1, 0], [0, 5, 7, 1, 7]]
    analyzer = RouteAnalyzer(matrix)
    analyzer._vertical_lines = {0, 1, 4}
    analyzer._horizontal_lines = {2}
    result = analyzer._get_min_value_from_undeleted_cells()

    assert result == 1


def test_get_intersection_points(example_matrix):
    analyzer = RouteAnalyzer(example_matrix)
    analyzer._vertical_lines = {0, 1, 4}
    analyzer._horizontal_lines = {2}
    result = [x for x in analyzer._get_intersection_points()]

    assert result == [(2, 0), (2, 1), (2, 4)]


def test_sum_value_at_intersection_points_cells():
    matrix = [[2, 4, 7, 2, 0], [0, 9, 7, 5, 4], [6, 7, 0, 0, 2], [2, 0, 1, 1, 0], [0, 5, 7, 1, 7]]
    expected_matrix = np.array(
        [[2, 4, 7, 2, 0], [0, 9, 7, 5, 4], [7, 8, 0, 0, 3], [2, 0, 1, 1, 0], [0, 5, 7, 1, 7]]
    )

    analyzer = RouteAnalyzer(matrix)
    analyzer._vertical_lines = {0, 1, 4}
    analyzer._horizontal_lines = {2}
    analyzer._sum_value_at_intersection_points_cells(1)

    assert np.array_equal(analyzer._matrix, expected_matrix)


def test_subtract_value_from_undeleted_cells():
    matrix = [[2, 4, 7, 2, 0], [0, 9, 7, 5, 4], [6, 7, 0, 0, 2], [2, 0, 1, 1, 0], [0, 5, 7, 1, 7]]
    expected_matrix = np.array(
        [[2, 4, 6, 1, 0], [0, 9, 6, 4, 4], [6, 7, 0, 0, 2], [2, 0, 0, 0, 0], [0, 5, 6, 0, 7]]
    )
    analyzer = RouteAnalyzer(matrix)
    analyzer._vertical_lines = {0, 1, 4}
    analyzer._horizontal_lines = {2}
    analyzer._subtract_value_from_undeleted_cells(1)

    assert np.array_equal(analyzer._matrix, expected_matrix)


def test_sum_and_subtract_minimum_value_from_selected_cells():
    matrix = [[2, 4, 7, 2, 0], [0, 9, 7, 5, 4], [6, 7, 0, 0, 2], [2, 0, 1, 1, 0], [0, 5, 7, 1, 7]]
    expected_matrix = np.array(
        [[2, 4, 6, 1, 0], [0, 9, 6, 4, 4], [7, 8, 0, 0, 3], [2, 0, 0, 0, 0], [0, 5, 6, 0, 7]]
    )
    analyzer = RouteAnalyzer(matrix)
    analyzer._vertical_lines = {0, 1, 4}
    analyzer._horizontal_lines = {2}
    analyzer._sum_and_subtract_minimum_value_from_selected_cells()

    assert np.array_equal(analyzer._matrix, expected_matrix)


@pytest.mark.parametrize(
    "cell, result",
    (((0, 0), True), ((1, 2), True), ((3, 3), True), ((4, 1), False), ((4, 4), False), ((5, 5), False)),
)
def test_is_a_valid_cell(cell, result, example_matrix):
    analyzer = RouteAnalyzer(example_matrix)

    assert analyzer._is_a_valid_cell(cell) is result


@pytest.mark.parametrize(
    "shape, chosen_cells, expected_result",
    (
        ((4, 4), [(0, 0), (1, 1), (2, 2), (3, 3)], [(0, 0), (1, 1), (2, 2), (3, 3)]),
        ((4, 3), [(0, 0), (1, 1), (2, 2), (3, 3)], [(0, 0), (1, 1), (2, 2)]),
    ),
)
def test_get_result(shape, chosen_cells, expected_result):
    matrix = np.zeros(shape)
    analyzer = RouteAnalyzer(matrix)
    analyzer._chosen_cells = chosen_cells

    assert analyzer._get_results() == expected_result


def test_get_combinations():
    matrix = [
        [9, 11, 14, 11, 7],
        [6, 15, 13, 13, 10],
        [12, 13, 6, 8, 8],
        [11, 9, 10, 12, 9],
        [7, 12, 14, 10, 14],
    ]
    analyzer = RouteAnalyzer(matrix)
    result = analyzer.get_combinations()

    assert result == [(0, 4), (1, 0), (4, 3), (3, 1), (2, 2)]


def test_get_combinations_with_unbalanced_matrix():
    matrix = [[9, 12, 11], [8, 13, 17], [20, 12, 13], [21, 15, 17]]
    analyzer = RouteAnalyzer(matrix)
    result = analyzer.get_combinations()

    assert result == [(1, 0), (0, 2), (2, 1)]


def test_get_combinations_with_matrix_with_multiple_solutions():
    matrix = [[5, 8, 2, 6], [8, 9, 3, 9], [4, 8, 1, 7], [12, 10, 4, 8]]
    analyzer = RouteAnalyzer(matrix)
    result = analyzer.get_combinations()

    assert result == [(0, 0), (2, 2), (3, 3), (1, 1)]


def test_get_combinations_with_complex_matrix(complex_matrix):
    analyzer = RouteAnalyzer(complex_matrix)
    result = analyzer.get_combinations()
    assert result == [(8, 0), (24, 1), (27, 2), (43, 3), (16, 4), (20, 5), (42, 6)]


def test_make_routes_combination(cargo_csv, trucks_csv, cargo, trucks):
    expected_result = {trucks[0]: cargo[0], trucks[1]: cargo[1]}
    result = RouteAnalyzer.make_routes_combination(cargo_csv, trucks_csv)
    assert result == expected_result
