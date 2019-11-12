import numpy as np
import pytest

from optimal_mapping.mapping import Mapping


@pytest.fixture
def matrix():
    return [
        [14, 12, 15, 15],
        [21, 18, 18, 22],
        [14, 17, 12, 14],
        [6, 5, 3, 6],
    ]


def test_rows_reductions(matrix):
    expected_result = np.array([[2, 0, 3, 3], [3, 0, 0, 4], [2, 5, 0, 2], [3, 2, 0, 3]])
    mapping = Mapping(matrix)
    mapping._rows_reductions()

    assert np.array_equal(mapping.matrix, expected_result)


def test_columns_subtraction(matrix):
    expected_result = np.array([[8, 7, 12, 9], [15, 13, 15, 16], [8, 12, 9, 8], [0, 0, 0, 0]])
    mapping = Mapping(matrix)
    mapping._columns_reductions()

    assert np.array_equal(mapping.matrix, expected_result)


def test_rows_scanning_doesnt_add_vertical_lines_if_zero_is_not_found():
    matrix = np.array([[2, 4], [1, 9],])
    mapping = Mapping(matrix)
    mapping._rows_scanning()

    assert mapping._vertical_lines == []


def test_rows_scanning_doesnt_add_vertical_lines_if_finds_more_than_one_zero():
    matrix = np.array([[2, 0, 4, 0, 1], [0, 1, 9, 0, 0]])
    mapping = Mapping(matrix)
    mapping._rows_scanning()

    assert mapping._vertical_lines == []


def test_rows_scanning():
    matrix = np.array([[2, 4, 7, 2, 0], [0, 9, 7, 5, 4], [6, 7, 0, 0, 2], [2, 0, 1, 1, 0], [0, 5, 7, 1, 7]])
    mapping = Mapping(matrix)
    mapping._rows_scanning()

    assert mapping._chosen_zeros == [(0, 4), (1, 0), (3, 1)]
    assert sorted(mapping._vertical_lines) == [0, 1, 4]
    assert mapping._zeros_scratched == {(0, 4), (3, 4), (1, 0), (4, 0), (3, 1)}


def test_columns_scanning_doesnt_cadd_horizontal_lines_if_zero_is_not_found():
    matrix = np.array([[2, 4], [1, 9]])
    mapping = Mapping(matrix)
    mapping._columns_scanning()

    assert mapping._horizontal_lines == []


def test_columns_scanning_doesnt_cadd_horizontal_lines_if_finds_more_than_one_zero():
    matrix = np.array([[2, 4, 0, 1], [1, 9, 5, 0], [7, 1, 0, 0], [2, 1, 9, 0]])
    mapping = Mapping(matrix)
    mapping._columns_scanning()

    assert mapping._horizontal_lines == []
