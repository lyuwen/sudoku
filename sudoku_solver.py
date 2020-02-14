import numpy as np


class SudokuSolver(object):
    """ Sudoku Solver
    """
    
    
    def __init__(self, grid, nsolutions=None):
        self.grid = np.array(grid)
        self.nsolutions = nsolutions


    def possible_f(self, x, y, num):
        if (self.grid[x, :] == num).any():
            return False
        if (self.grid[:, y] == num).any():
            return False
        x0 = (x // 3) * 3
        y0 = (y // 3) * 3
        if (self.grid[x0:x0 + 3, y0:y0 + 3] == num).any():
            return False
        return True


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
    
    
    def solve(self, method=2):
        self.solutions = []
        if method == 0:
            self._solve_v1_a()
        elif method == 1:
            self._solve_v1_b()
        elif method == 2:
            self._solve_v2()

    
    def _solve_v1_a(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i, j] == 0:
                    for n in range(1, 10):
                        if self.possible_f(i, j, n):
                            self.grid[i, j] = n
                            self._solve_v1_a()
                            self.grid[i, j] = 0
                    return
        self.solutions.append(self.grid.copy())

        
    def _solve_v1_b(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i, j] == 0:
                    for n in range(1, 10):
                        if self.possible(i, j, n):
                            self.grid[i, j] = n
                            self._solve_v1_b()
                            self.grid[i, j] = 0
                    return
        self.solutions.append(self.grid.copy())


    def _solve_v2(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i, j] == 0:
                    for n in self.possibilities(i, j):
                        self.grid[i, j] = n
                        self._solve_v2()
                        self.grid[i, j] = 0
                    return
        self.solutions.append(self.grid.copy())


    def solven(self, nsolutions=None):
        self.solutions = []
        if nsolutions is not None:
          self.nsolutions = nsolutions
        self._solven()


    def _solven(self):
        if self.nsolutions is not None and len(self.solutions) >= self.nsolutions:
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
