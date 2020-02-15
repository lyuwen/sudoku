from __future__ import print_function
import numpy as np

from sudoku.generic_sudoku_solver import GenericSudokuSolver


class GenericSudoku(GenericSudokuSolver):

    def __init__(self, dim, rank, timeout=1):
        shape = (dim**rank, ) * rank
        super().__init__(
            grid=np.zeros(shape, int),
            dim=dim,
            rank=rank,
            timeout=timeout
        )
        self.token = np.arange(self.nnumbers + 1)

    def random_grid(self, nrandomsteps=5):
        self.grid = np.zeros((self.nnumbers, ) * self.rank, int)
        valid_steps = 0
        while valid_steps < nrandomsteps:
            rand_index = tuple(np.random.randint(
                0, self.nnumbers, size=(self.rank, )))
            if self.grid[rand_index] == 0:
                rand_num = np.random.randint(1, self.nnumbers + 1)
                self.grid[rand_index] = rand_num
                if (self.grid_is_valid and self.grid_is_solvable):
                    valid_steps += 1
                else:
                    self.grid[rand_index] = 0
        self.solve(1)
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
        if not self.is_valid(grid, dim=self.dim, rank=self.rank):
            raise ValueError(
                "Input grid does not satisfy the basic rules of Sudoku.")
        self.grid = grid

    def copy(self):
        new = self.__class__(dim=self.dim, rank=self.rank)
        new.set_grid(self.grid.copy())
        new.token = self.token.copy()
        if hasattr(self, "random_seed"):
            new.random_seed = self.random_seed.copy()
        return new
