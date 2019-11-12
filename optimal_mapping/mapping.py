# python 3.8.0
import numpy as np


class Mapping:
    def __init__(self, matrix):
        self.matrix = np.array(matrix)
        self.matrix_size = len(self.matrix)
        self._chosen_zeros = list()
        self._vertical_lines = list()
        self._horizontal_lines = list()
        self._zeros_scratched = set()

    # Phase 1: Rows and Columns reductions
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

    # Phase 2: Optimization of the problem
    # Step 01: Draw a minimum numbers of lines to cover all the zeros of the matrix
    # Procedure
    # a) Row Scanning
    # i) Starting from the first row, ask the question: is the exactly one zero in that row? If yes, make
    # a square around that zero and draw a vertical line passing through that zero; Otherwise skip that row.
    # ii) After scanning the last row, check whether all the zeros are covered with lines. If yes, go to Step 2;
    # Otherwise, do column scanning.
    # b) Column Scanning
    # i) Starting from the first column, ask the question: is the exactly one zero in that column? If yes, make
    # a square around that zero and draw a horizontal line passing through that zero; Otherwise skip that column.
    # ii) After scanning the last column, check whether all the zeros are covered with lines.
    #
    # Step 02:

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





    ########################## !!!!!!!!!!!!!!!! ATENCAO
    # No scanning horizontal além da condicao if 0 < len((zero_index := np.where(column == 0)[0])) < 2: tem que ver o zero foi riscado.
    # Pensando agora por esse mesmo motivo precisa guardar as posicões dos zeros sublinhados, pra não sublinhar duas vezes

    def _total_zero_values(self):
        return self.matrix_size * self.matrix_size - np.count_nonzero(self.matrix)
