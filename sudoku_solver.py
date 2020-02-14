import numpy as np


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
        possibilities = set(range(0, 10)) - existing
        return sorted(possibilities)
    
    
    def solve(self, method=0):
        """ Solve for all solutions for a given Sudoku grid
        """
        self.solutions = []
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


    def _solve(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i, j] == 0:
                    for n in self.possibilities(i, j):
                        self.grid[i, j] = n
                        self._solve()
                        self.grid[i, j] = 0
                    return
        self.solutions.append(self.grid.copy())


    def solven(self, nsolutions=None):
        """ Solve for up to the first N solutions of a given Sudoku grid.
        """
        self.solutions = []
        if nsolutions is not None:
          self._nsolutions = nsolutions
        self._solven()


    def _solven(self):
        if self._nsolutions is not None and len(self.solutions) >= self._nsolutions:
            return
        for i in range(9):
            for j in range(9):
                if self.grid[i, j] == 0:
                    for n in self.possibilities(i, j):
                        self.grid[i, j] = n
                        self._solven()
                        self.grid[i, j] = 0
                    return
        self.solutions.append(self.grid.copy())
