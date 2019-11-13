# python 3.8.0
import numpy as np

# Renomear para RouteAnalizer?
class Mapping:
    def __init__(self, matrix):
        self.matrix = np.array(matrix)
        self.matrix_size = len(self.matrix)
        self._chosen_zeros = list()
        self._vertical_lines = list()
        self._horizontal_lines = list()
        self._zeros_scratched = set()

    @property
    def total_zero_values(self):
        return self.matrix_size ** 2 - np.count_nonzero(self.matrix)

    def run(self):
        # Phase 1
        self.matrix_reduction()

        # Phase 2
        while True:
            self.matrix_scanning()

            if len(self._chosen_zeros) == self.matrix_size:
                break

            self.sum_and_subtract_minimum_value_from_selected_cells()

        return self._chosen_zeros

    def matrix_reduction(self):
        self._rows_reductions()
        self._columns_reductions()

    def matrix_scanning(self):
        self._reset_scanning_values()

        while len(self._zeros_scratched) != self.total_zero_values:
            self._rows_scanning()
            if len(self._zeros_scratched) == self.total_zero_values:
                break
            self._columns_scanning()

    def sum_and_subtract_minimum_value_from_selected_cells(self):
        min_value = self._get_min_value_from_undeleted_cells()
        self._sum_value_at_intersection_points(min_value)
        self._subtract_value_from_undeleted_cells(min_value)

    def _rows_reductions(self):
        for row in self.matrix:
            min_value = min(row)
            for i in range(self.matrix_size):
                row[i] -= min_value

    def _columns_reductions(self):
        for column in self.matrix.transpose():
            min_value = min(column)
            for i in range(self.matrix_size):
                column[i] -= min_value


    def _rows_scanning(self):
        for x, row in enumerate(self.matrix):
            zeros_from_row = [(x, y) for y in np.where(row == 0)[0]]
            zeros_from_row = [zero for zero in zeros_from_row if zero not in self._zeros_scratched]

            if len(zeros_from_row) != 1:
                continue

            chosen_zero = zeros_from_row.pop()
            vertical_line = chosen_zero[1]
            self._chosen_zeros.append(chosen_zero)
            self._vertical_lines.append(vertical_line)

            column = self.matrix.transpose()[vertical_line]
            zeros_from_column = np.where(column == 0)[0]
            self._zeros_scratched |= {(x, vertical_line) for x in zeros_from_column}

    def _columns_scanning(self):
        for y, column in enumerate(self.matrix.transpose()):
            zeros_from_column = [(x, y) for x in np.where(column == 0)[0]]
            zeros_from_column = [zero for zero in zeros_from_column if zero not in self._zeros_scratched]

            if len(zeros_from_column) != 1:
                continue

            chosen_zero = zeros_from_column.pop()
            horizontal_line = chosen_zero[0]
            self._chosen_zeros.append(chosen_zero)
            self._horizontal_lines.append(horizontal_line)

            row = self.matrix[horizontal_line]
            zeros_from_row = np.where(row == 0)[0]
            self._zeros_scratched |= {(horizontal_line, y) for y in zeros_from_row}

    def _reset_scanning_values(self):
        self._chosen_zeros = list()
        self._vertical_lines = list()
        self._horizontal_lines = list()
        self._zeros_scratched = set()

    # Step 3: Identify the min value of the undeleted cell values
    # a) add the min undeleted value at the intersection points of the present matrix
    # b) subtract the minimum undeleted cell value from all the undeleted cell values
    # c) All other entries remain the same
    # Step 4: Start phase 2 again


    @property
    def _intersection_points(self):
        return {(x, y) for x in self._horizontal_lines for y in self._vertical_lines}

    def _sum_value_at_intersection_points(self, value):
        for point in self._intersection_points:
            self.matrix[point[0]][point[1]] += value

    def _get_undeleted_cells(self):
        clear_rows = [row for row in range(self.matrix_size) if row not in self._horizontal_lines]
        clear_columns = [column for column in range(self.matrix_size) if column not in self._vertical_lines]

        return [(x, y) for x in clear_rows for y in clear_columns]

    def _get_min_value_from_undeleted_cells(self):
        return min([self.matrix[cell[0]][cell[1]] for cell in self._get_undeleted_cells()])

    def _subtract_value_from_undeleted_cells(self, value):
        for cell in self._get_undeleted_cells():
            self.matrix[cell[0]][cell[1]] -= value
