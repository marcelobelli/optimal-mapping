# python 3.8.0
import numpy as np

from optimal_mapping.helpers import get_cargo, get_distance_between, get_trucks


class RouteAnalyzer:
    def __init__(self, matrix):
        self._matrix = np.array(matrix)
        self._original_matrix_shape = self._matrix.shape

        self._chosen_cells = list()
        self._vertical_lines = list()
        self._horizontal_lines = list()
        self._zeros_scratched = set()

    @property
    def _total_zero_values(self):
        return self._matrix.size - np.count_nonzero(self._matrix)

    def get_combinations(self):
        self._balance_matrix()
        self._matrix_reduction()

        while True:
            self._matrix_scanning()

            if len(self._chosen_cells) == self._matrix.shape[0]:
                break

            self._sum_and_subtract_minimum_value_from_selected_cells()

        return self._get_results()

    def _balance_matrix(self):
        rows, columns = self._original_matrix_shape

        if rows == columns:
            return

        self._matrix = (
            self._get_matrix_with_dummy_rows() if rows < columns else self._get_matrix_with_dummy_columns()
        )

    def _get_matrix_with_dummy_rows(self):
        rows, columns = self._original_matrix_shape
        diff_between_rows_and_columns = columns - rows
        rows_to_add = np.zeros((diff_between_rows_and_columns, columns))
        return np.row_stack((self._matrix, rows_to_add))

    def _get_matrix_with_dummy_columns(self):
        rows, columns = self._original_matrix_shape
        diff_between_columns_and_rows = rows - columns
        columns_to_add = np.zeros((rows, diff_between_columns_and_rows))
        return np.column_stack((self._matrix, columns_to_add))

    def _matrix_reduction(self):
        self._make_reductions(self._matrix)
        self._make_reductions(self._matrix.transpose())

    def _make_reductions(self, matrix):
        for values in matrix:
            min_value = min(values)
            for i in range(self._matrix.shape[0]):
                values[i] -= min_value

    def _matrix_scanning(self):
        self._reset_scanning_values()

        while len(self._zeros_scratched) != self._total_zero_values:
            row_scanning_successful = self._rows_scanning()
            if len(self._zeros_scratched) == self._total_zero_values:
                break
            column_scanning_successful = self._columns_scanning()

            if not row_scanning_successful and not column_scanning_successful:
                self._random_scanning()

    def _reset_scanning_values(self):
        self._chosen_cells = list()
        self._vertical_lines = list()
        self._horizontal_lines = list()
        self._zeros_scratched = set()

    def _rows_scanning(self):
        scanning_result = False
        for x, row in enumerate(self._matrix):
            if x in self._horizontal_lines:
                continue

            zeros_in_row = [(x, y) for y in np.where(row == 0)[0] if (x, y) not in self._zeros_scratched]

            if len(zeros_in_row) != 1:
                continue

            scanning_result = True
            chosen_zero = zeros_in_row.pop()
            _, vertical_line = chosen_zero
            self._chosen_cells.append(chosen_zero)
            self._vertical_lines.append(vertical_line)

            column = self._matrix.transpose()[vertical_line]
            zeros_from_column = np.where(column == 0)[0]
            self._zeros_scratched |= {(x, vertical_line) for x in zeros_from_column}

        return scanning_result

    def _columns_scanning(self):
        scanning_result = False
        for y, column in enumerate(self._matrix.transpose()):
            if y in self._vertical_lines:
                continue

            zeros_in_column = [
                (x, y) for x in np.where(column == 0)[0] if (x, y) not in self._zeros_scratched
            ]

            if len(zeros_in_column) != 1:
                continue

            scanning_result = True
            chosen_zero = zeros_in_column.pop()
            horizontal_line, _ = chosen_zero
            self._chosen_cells.append(chosen_zero)
            self._horizontal_lines.append(horizontal_line)

            row = self._matrix[horizontal_line]
            zeros_from_row = np.where(row == 0)[0]
            self._zeros_scratched |= {(horizontal_line, y) for y in zeros_from_row}

        return scanning_result

    def _random_scanning(self):
        for x, row in enumerate(self._matrix):
            if x in self._horizontal_lines:
                continue

            zeros_from_row = [(x, y) for y in np.where(row == 0)[0] if (x, y) not in self._zeros_scratched]

            if len(zeros_from_row) == 0:
                continue

            chosen_zero = zeros_from_row[0]
            horizontal_line, vertical_line = chosen_zero
            self._chosen_cells.append(chosen_zero)
            self._vertical_lines.append(vertical_line)
            self._horizontal_lines.append(horizontal_line)

            column = self._matrix.transpose()[vertical_line]
            zeros_from_column = np.where(column == 0)[0]
            self._zeros_scratched |= {(x, vertical_line) for x in zeros_from_column}
            self._zeros_scratched |= {zero for zero in zeros_from_row}

            break

    def _get_results(self):
        if len(set(self._original_matrix_shape)) == 1:
            return self._chosen_cells

        return [cell for cell in self._chosen_cells if self._is_a_valid_cell(cell)]

    def _is_a_valid_cell(self, cell):
        cell_row, cell_column = cell
        rows, columns = self._original_matrix_shape

        return cell_row < rows and cell_column < columns

    def _sum_and_subtract_minimum_value_from_selected_cells(self):
        min_value = self._get_min_value_from_undeleted_cells()
        self._sum_value_at_intersection_points_cells(min_value)
        self._subtract_value_from_undeleted_cells(min_value)

    def _get_min_value_from_undeleted_cells(self):
        return min([self._matrix[cell[0]][cell[1]] for cell in self._get_undeleted_cells()])

    def _get_undeleted_cells(self):
        rows, columns = self._matrix.shape
        clear_rows = [row for row in range(rows) if row not in self._horizontal_lines]
        clear_columns = [column for column in range(columns) if column not in self._vertical_lines]
        return ((x, y) for x in clear_rows for y in clear_columns)

    def _sum_value_at_intersection_points_cells(self, value):
        for point in self._get_intersection_points():
            self._matrix[point[0]][point[1]] += value

    def _get_intersection_points(self):
        return ((x, y) for x in self._horizontal_lines for y in self._vertical_lines)

    def _subtract_value_from_undeleted_cells(self, value):
        for cell in self._get_undeleted_cells():
            self._matrix[cell[0]][cell[1]] -= value

    @classmethod
    def make_routes_combination(cls, cargo_csv, trucks_csv):
        cargo = get_cargo(cargo_csv)
        trucks = get_trucks(trucks_csv)
        matrix = [[get_distance_between(load, truck) for load in cargo] for truck in trucks]
        analyzer = cls(matrix)
        combinations = analyzer.get_combinations()

        return {trucks[x]: cargo[y] for x, y in combinations}
