# python 3.8.0
import numpy as np

from time import sleep


class RouteAnalyzer:
    def __init__(self, matrix):
        self.matrix = self.get_stabilized_matrix(matrix)
        self.matrix_size = len(self.matrix)

        ##############################################
        #  Refatorar essa porra: https://docs.scipy.org/doc/numpy/reference/arrays.ndarray.html
        # Usar o .shape
        self._original_matrix_dimension = (len(matrix), len(matrix[0]))
        self._chosen_zeros = list()
        self._vertical_lines = list()
        self._horizontal_lines = list()
        self._zeros_scratched = set()


    @property
    def total_zero_values(self):
        return self.matrix_size ** 2 - np.count_nonzero(self.matrix)

    def get_stabilized_matrix(self, matrix):
        matrix = np.array(matrix)
        rows = len(matrix)
        columns = len(matrix.transpose())

        if rows == columns:
            return matrix

        ################################################################
        ###################################################################
        ###################################################################
        # Nome das funcões: add_dummy_rows e add_dummy_columns
        # Preciso de alguma forma controlar isso pra no fim excluir os dummies do resultado
        # Talvez um range com passo negativo, sei lá
        # Soma do indice mais a diferenca não pode dar maior que a coordenada
        if rows < columns:
            diff_between_rows_and_columns = columns - rows
            rows_to_add = np.zeros((diff_between_rows_and_columns, columns))
            return np.row_stack((matrix, rows_to_add))

        diff_between_columns_and_rows = rows - columns
        columns_to_add = np.zeros((rows, diff_between_columns_and_rows))
        return np.column_stack((matrix, columns_to_add))

    def run(self):
        self.matrix_reduction()

        while True:
            self.matrix_scanning()

            if len(self._chosen_zeros) == self.matrix_size:
                break

            self.sum_and_subtract_minimum_value_from_selected_cells()

        self._clean_chosen_zeros()
        # print("###############################################")
        # print(self._original_matrix_dimension)
        return self._chosen_zeros

    def _clean_chosen_zeros(self):
        if len(set(self._original_matrix_dimension)) == 1:
            return

        self._chosen_zeros = [cell for cell in self._chosen_zeros if cell[0] < self._original_matrix_dimension[0] and cell[1] < self._original_matrix_dimension[1]]


        # for cell in self._chosen_zeros:
        #     if cell[0] < self._original_matrix_dimension[0] and cell[1] < self._original_matrix_dimension[1]:
        #         print(f"CELL: {cell[0]} < {self._original_matrix_dimension[0]} and {cell[1]} < {self._original_matrix_dimension[1]}")
        #         sleep(3)
        #         continue
        #     self._chosen_zeros.remove(cell)

    def matrix_reduction(self):
        self._rows_reductions()
        self._columns_reductions()

    def matrix_scanning(self):
        self._reset_scanning_values()

        while len(self._zeros_scratched) != self.total_zero_values:
            row_scanning_successful = self._rows_scanning()
            if len(self._zeros_scratched) == self.total_zero_values:
                break
            column_scanning_successful = self._columns_scanning()

            if not row_scanning_successful or not column_scanning_successful:
                self._random_scanning()


    def sum_and_subtract_minimum_value_from_selected_cells(self):
        min_value = self._get_min_value_from_undeleted_cells()
        self._sum_value_at_intersection_points_cells(min_value)
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

    def _reset_scanning_values(self):
        self._chosen_zeros = list()
        self._vertical_lines = list()
        self._horizontal_lines = list()
        self._zeros_scratched = set()

    def _rows_scanning(self):
        scanning_result = False
        for x, row in enumerate(self.matrix):
            if x in self._horizontal_lines:
                continue

            zeros_from_row = [(x, y) for y in np.where(row == 0)[0]]
            zeros_from_row = [zero for zero in zeros_from_row if zero not in self._zeros_scratched]

            if len(zeros_from_row) != 1:
                continue
            
            scanning_result = True
            chosen_zero = zeros_from_row.pop()
            vertical_line = chosen_zero[1]
            self._chosen_zeros.append(chosen_zero)
            self._vertical_lines.append(vertical_line)

            column = self.matrix.transpose()[vertical_line]
            zeros_from_column = np.where(column == 0)[0]
            self._zeros_scratched |= {(x, vertical_line) for x in zeros_from_column}
        
        return scanning_result

    def _columns_scanning(self):
        scanning_result = False
        for y, column in enumerate(self.matrix.transpose()):
            if y in self._vertical_lines:
                continue

            zeros_from_column = [(x, y) for x in np.where(column == 0)[0]]
            zeros_from_column = [zero for zero in zeros_from_column if zero not in self._zeros_scratched]

            if len(zeros_from_column) != 1:
                continue

            scanning_result = True
            chosen_zero = zeros_from_column.pop()
            horizontal_line = chosen_zero[0]
            self._chosen_zeros.append(chosen_zero)
            self._horizontal_lines.append(horizontal_line)

            row = self.matrix[horizontal_line]
            zeros_from_row = np.where(row == 0)[0]
            self._zeros_scratched |= {(horizontal_line, y) for y in zeros_from_row}

        return scanning_result

    def _get_min_value_from_undeleted_cells(self):
        return min([self.matrix[cell[0]][cell[1]] for cell in self._get_undeleted_cells()])

    def _sum_value_at_intersection_points_cells(self, value):
        for point in self._get_intersection_points():
            self.matrix[point[0]][point[1]] += value

    def _get_intersection_points(self):
        return ((x, y) for x in self._horizontal_lines for y in self._vertical_lines)

    def _subtract_value_from_undeleted_cells(self, value):
        for cell in self._get_undeleted_cells():
            self.matrix[cell[0]][cell[1]] -= value

    def _get_undeleted_cells(self):
        clear_rows = [row for row in range(self.matrix_size) if row not in self._horizontal_lines]
        clear_columns = [column for column in range(self.matrix_size) if column not in self._vertical_lines]
        return ((x, y) for x in clear_rows for y in clear_columns)

    def _random_scanning(self):
        for x, row in enumerate(self.matrix):
            ###### Macete interessante pra não ficar escaneando row e column já riscado
            if x in self._horizontal_lines:
                continue

            zeros_from_row = [(x, y) for y in np.where(row == 0)[0]]
            zeros_from_row = [zero for zero in zeros_from_row if zero not in self._zeros_scratched]

            if len(zeros_from_row) == 0:
                continue

            chosen_zero = zeros_from_row.pop(0)
            vertical_line = chosen_zero[1]
            horizontal_line = chosen_zero[0]
            self._chosen_zeros.append(chosen_zero)
            self._vertical_lines.append(vertical_line)
            self._horizontal_lines.append(horizontal_line)

            column = self.matrix.transpose()[vertical_line]
            row = self.matrix[horizontal_line]
            zeros_from_column = np.where(column == 0)[0]
            zeros_from_row = np.where(row == 0)[0]
            self._zeros_scratched |= {(x, vertical_line) for x in zeros_from_column}
            self._zeros_scratched |= {(horizontal_line, y) for y in zeros_from_row}

            break
