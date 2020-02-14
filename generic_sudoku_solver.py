import numpy as np

from utils import timeout
from constants import get_sudoku_neighbor_list


class GenericSudokuSolver(object):

    def __init__(self, grid, dim=None, rank=None):
        self.grid = np.array(grid)
        if ((dim is not None) and (rank is not None)):
            # check dimension
            if ((len(self.grid.shape) != rank)
                    or (self.grid.shape != (dim**rank, ) * rank)):
                raise ValueError("Shape of input variable grid "
                                 "does not match input dim and rank")
            self.dim = dim
            self.rank = rank
        elif ((dim is None) and (rank is None)):
            self.rank = len(self.grid.shape)
            self.dim = np.round(
                self.grid.shape[0] ** (1./self.rank)).astype(int)
            if self.grid.shape != (self.dim**self.rank, ) * self.rank:
                raise ValueError(
                    "Input dim and rank does not match the shape of grid.")
        else:
            raise ValueError(
                "Input dim and rank should either both or neither exist.")
        self._neighbor_list = get_sudoku_neighbor_list(
            dim=self.dim, rank=self.rank)

    @property
    def nnumbers(self):
        return self.dim ** self.rank

    @property
    def neighbor_list(self):
        return self._neighbor_list

    def copy(self):
        return self.__class__(
            grid=self.grid.copy(),
            dim=self.dim,
            rank=self.rank
        )

    def possibilities(self, index):
        if self.grid[index] != 0:
            return []
        existing = set(self.grid[tuple(self.neighbor_list[index].T)])
        possibilities = set(range(1, self.nnumbers + 1)) - existing
        return sorted(possibilities)

    def possibility_map(self):
        return np.array([len(self.possibilities(index)) for index in np.ndindex(*self.grid.shape)]).reshape(self.grid.shape)

    def solve(self, nsolutions=None):
        """ Solve for up to the first N solutions of a given Sudoku grid.
        """
        self.solutions = []
        self.solutions_depth = []
        self._nsolutions = nsolutions
        self._solve(0)

    def _solve(self, depth=0):
        if self._nsolutions is not None and len(self.solutions) >= self._nsolutions:
            return
        for index in zip(*(self.grid == 0).nonzero()):
            for n in self.possibilities(index):
                depth += 1
                self.grid[index] = n
                self._solve(depth=depth)
                self.grid[index] = 0
            return
        self.solutions.append(self.grid.copy())
        self.solutions_depth.append(depth)


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
    gs = GenericSudokuSolver(grid=grid)
    print gs.dim
    print gs.rank
    print gs.nnumbers
    print gs.grid
    print gs.possibilities((4, 4))
    print gs.possibility_map()
    gs.solve()
    print gs.solutions
    print gs.solutions_depth
