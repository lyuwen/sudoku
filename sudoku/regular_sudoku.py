from __future__ import print_function
import numpy as np

from sudoku.regular_sudoku_solver import RegularSudokuSolver


class RegularSudoku(RegularSudokuSolver):

    def __init__(self):
        super().__init__(np.zeros((9, 9), int))
        self.token = np.arange(10)

    def random_grid(self, nrandomsteps=5):
        self.grid = np.zeros((9, 9), int)
        valid_steps = 0
        while valid_steps < nrandomsteps:
            oldgrid = self.grid.copy()
            self.grid[np.random.randint(9), np.random.randint(
                9)] = np.random.randint(1, 10)
            if (self.is_valid(self.grid) and self.grid_is_solvable):
                valid_steps += 1
            else:
                self.grid = oldgrid
        self.solven(1)
        self.seed_grid = self.grid.copy()
        self.grid = self.solutions[0]
        return self.grid

    def randomize_token(self):
        np.random.shuffle(self.token[1:])
        return self.get_tokenized_grid()

    def get_tokenized_grid(self):
        return self.token[self.grid.flatten()].reshape(self.grid.shape)

    def set_grid(self, grid):
        grid = np.array(grid)
        if not self.is_valid(grid):
            raise ValueError(
                "Input grid does not satisfy the basic rules of Sudoku.")
        self.grid = grid

    def copy(self):
        new = self.__class__()
        new.set_grid(self.grid.copy())
        new.token = self.token.copy()
        if hasattr(self, "seed_grid"):
            new.seed_grid = self.seed_grid.copy()
        return new
