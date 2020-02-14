from __future__ import print_function
import numpy as np

from utils import timeout, count_nonzero_unique
from constants import sudoku_neighbor_list


class SudokuSolver(object):
    """ Sudoku Solver
    """

    def __init__(self, grid):
        self.grid = np.array(grid)

    def possible(self, x, y, num):
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        for i in range(9):
            if self.grid[x, i] == num:
                return False
            if self.grid[i, y] == num:
                return False
        for i in range(3):
            for j in range(3):
                if self.grid[x0 + i, y0 + j] == num:
                    return False
        return True

    def possibilities(self, x, y):
        if self.grid[x, y] != 0:
            return []
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        existing = set()
        existing |= set(self.grid[x, :])
        existing |= set(self.grid[:, y])
        existing |= set(self.grid[x0:x0 + 3, y0:y0 + 3].flatten())
        possibilities = set(range(1, 10)) - existing
        return sorted(possibilities)

    def solve(self, method=0):
        """ Solve for all solutions for a given Sudoku grid
        """
        self.solutions = []
        self.solutions_depth = []
        if method == 0:
            self._solve()
        elif method == 1:
            self._solve_alt()
        else:
            raise ValueError("Invalid method number, expected to be either 0 or 1.")

    def _solve_alt(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i, j] == 0:
                    for n in range(1, 10):
                        if self.possible(i, j, n):
                            self.grid[i, j] = n
                            self._solve_alt()
                            self.grid[i, j] = 0
                    return
        self.solutions.append(self.grid.copy())

    def _solve(self, depth=0):
        for i, j in zip(*(self.grid == 0).nonzero()):
            for n in self.possibilities(i, j):
                depth += 1
                self.grid[i, j] = n
                self._solve(depth=depth)
                self.grid[i, j] = 0
            return
        self.solutions.append(self.grid.copy())
        self.solutions_depth.append(depth)

    def solven(self, nsolutions=None):
        """ Solve for up to the first N solutions of a given Sudoku grid.
        """
        self.solutions = []
        self.solutions_depth = []
        self._nsolutions = nsolutions
        self._solven(0)

    def _solven(self, depth=0):
        if self._nsolutions is not None and len(self.solutions) >= self._nsolutions:
            return
        for i, j in zip(*(self.grid == 0).nonzero()):
            for n in self.possibilities(i, j):
                depth += 1
                self.grid[i, j] = n
                self._solven(depth=depth)
                self.grid[i, j] = 0
            return
        self.solutions.append(self.grid.copy())
        self.solutions_depth.append(depth)

    def possibility_map(self):
        return np.array([[len(self.possibilities(i, j)) for j in range(9)] for i in range(9)])

    @staticmethod
    def is_valid(grid):
        grid = np.array(grid)
        for i in range(9):
            counts = count_nonzero_unique(grid[i, :])
            if (counts > 1).any():
                return False
            counts = count_nonzero_unique(grid[:, i])
            if (counts > 1).any():
                return False
        for i in range(3):
            for j in range(3):
                counts = count_nonzero_unique(grid[i * 3:i * 3 + 3, j * 3:j * 3 + 3].flatten())
                if (counts > 1).any():
                    return False
        return True

    @property
    def grid_is_valid(self):
        return self.is_valid(self.grid)

    @property
    def grid_is_solvable(self):
        if not self.grid_is_valid:
          return False
        is_solvable = False
        with timeout(1):
            self.solven(1)
            is_solvable = True
        return is_solvable

    @property
    def grid_is_solution_unique(self):
        if not self.grid_is_valid:
          return False
        is_solvable = False
        with timeout(1):
            self.solven(2)
            is_solvable = True
        return len(self.solutions) == 1

    @property
    def neighbor_list(self):
        return sudoku_neighbor_list

    def copy(self):
        return self.__class__(self.grid.copy())


if __name__ == "__main__":
    grid = np.array(
        [[5, 3, 0, 0, 7, 0, 0, 0, 0],
         [6, 0, 0, 1, 9, 5, 0, 0, 0],
         [0, 9, 8, 0, 0, 0, 0, 6, 0],
         [8, 0, 0, 0, 6, 0, 0, 0, 3],
         [4, 0, 0, 8, 0, 3, 0, 0, 1],
         [7, 0, 0, 0, 2, 0, 0, 0, 6],
         [0, 6, 0, 0, 0, 0, 2, 8, 0],
         [0, 0, 0, 4, 1, 9, 0, 0, 5],
         [0, 0, 0, 0, 8, 0, 0, 7, 9]])
    s = SudokuSolver(grid=grid)
    s.solve()
    print(s.possibility_map())
    print(s.solutions)
    print(s.solutions_depth)
    #  print(s.neighbor_list.shape)
