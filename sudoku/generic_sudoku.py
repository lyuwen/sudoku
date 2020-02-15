from __future__ import print_function
import numpy as np

from sudoku.generic_sudoku_solver import GenericSudokuSolver


class GenericSudoku(GenericSudokuSolver):

    def __init__(self, dim, rank):
        shape = (dim**rank, ) * rank
        super().__init__(np.zeros(shape, int))
        self.token = np.arange(self.nnumbers + 1)

    def random_grid(self, nrandomsteps=5):
        self.grid = np.zeros((self.nnumbers, ) * self.rank, int)
        valid_steps = 0
        while valid_steps <= nrandomsteps:
            oldgrid = self.grid.copy()
            self.grid[tuple(np.random.randint(self.nnumbers, size=(self.rank, )))] = np.random.randint(1, self.nnumbers + 1)
            is_solvable = False
            if self.grid_is_valid and self.grid_is_solvable:
                is_solvable = True
                valid_steps += 1
            if not is_solvable:
                self.grid = oldgrid
                valid_steps = nrandomsteps
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
            raise ValueError("Input grid does not satisfy the basic rules of Sudoku.")
        self.grid = grid

    def copy(self):
        new = self.__class__(dim=self.dim, rank=self.rank)
        new.set_grid(self.grid.copy())
        new.token = self.token.copy()
        if hasattr(self, "random_seed"):
            new.random_seed = self.random_seed.copy()
        return new


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
    #  s = GenericSudoku(dim=3, rank=2)
    #  s.set_grid(grid)
    #  s.solve()
    #  print(s.possibility_map())
    #  print(s.solutions)
    #  print(s.solutions_depth)
    #  print(s.grid_is_valid)
    #  print(s.grid_is_solvable)
    #  print(s.grid_is_solution_unique)

    #  nonzero_x, nonzero_y = s.grid.nonzero()
    #  print("nonzero_x", nonzero_x)
    #  print("nonzero_y", nonzero_y)
    #  single_x, single_y = (s.possibility_map() == 1).nonzero()
    #  print("single_x", single_x)
    #  print("single_y", single_y)
    #  print(grid[tuple(s.neighbor_list[4, 4].T)].nonzero()[0])
    #  print()
    #  print("remove x, remove y, grid solvable, grid solution unique, possibility > 1, solutions depth")
    #  for i, j in s.neighbor_list[4, 4][grid[tuple(s.neighbor_list[4, 4].T)].nonzero()[0], :]:
    #      sprime = s.copy()
    #      sprime.grid[i, j] = 0
    #      print(i, j, sprime.grid_is_solvable, sprime.grid_is_solution_unique, sprime.possibility_map()[4, 4] > 1, sprime.solutions_depth)
    #

    s = GenericSudoku(dim=3, rank=2)
    #  s = GenericSudoku(dim=2, rank=2)
    #  s = GenericSudoku(dim=2, rank=3)
    #  raise SystemExit
    #  print(s.grid_is_valid)
    #  print(s.grid_is_solvable)
    #  print(s.grid_is_solution_unique)
    s.random_grid(nrandomsteps=-1)
    #  print(s.grid)
    #  s.solve(1)
    #  print(self.nnumbers)
    print(s.grid.shape)
    #  print(s.grid)
    print(np.count_nonzero(s.grid))
    print(s.grid_is_valid)
    print(s.grid_is_solvable)
    s.solve(1)
    print(len(s.solutions))
    #  print(s.grid[:2, :2, :2])
    #  print(s.grid[:, 1, 0])
    #  print(s.neighbor_list[0, 0, 0])
    #  print(s.seed_grid)
