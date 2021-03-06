from __future__ import print_function
import numpy as np

from sudoku.utils import timeout, count_nonzero_unique
from sudoku.constants import get_sudoku_neighbor_list


class GenericSudokuSolver(object):

    def __init__(self, grid, dim=None, rank=None, timeout=1):
        self.grid = np.array(grid)
        self.timeout = timeout
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

    @staticmethod
    def is_valid(grid, dim, rank):
        nnumbers = dim ** rank
        grid = np.array(grid)
        for j in range(rank):
            for i in np.ndindex((nnumbers, ) * (rank - 1)):
                slices = i[:j] + (slice(None), ) + i[j:]
                counts = count_nonzero_unique(grid[slices])
                if (counts > 1).any():
                    return False
        for major_index in np.ndindex((dim, ) * rank):
            slices = tuple([slice(i * dim, i * dim + dim)
                            for i in major_index])
            counts = count_nonzero_unique(grid[slices].flatten())
            if (counts > 1).any():
                return False
        return True

    @property
    def grid_is_valid(self):
        return self.is_valid(self.grid, dim=self.dim, rank=self.rank)

    @property
    def grid_is_solvable(self):
        if not self.grid_is_valid:
            return False
        original_grid = self.grid.copy()
        with timeout(self.timeout):
            self.solve(1)
        self.grid = original_grid
        return len(self.solutions) == 1

    @property
    def grid_is_solution_unique(self):
        if not self.grid_is_valid:
            return False
        original_grid = self.grid.copy()
        with timeout(self.timeout):
            self.solve(2)
        self.grid = original_grid
        return len(self.solutions) == 1
