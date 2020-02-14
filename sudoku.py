import numpy as np

from utils import timeout
from sudoku_solver import SudokuSolver


def count_nonzero_unique(arr):
    unique, counts = np.unique(arr, return_counts=True)
    return counts[unique.nonzero()]


class Sudoku(SudokuSolver):
    
    
    def __init__(self, nrandomsteps=5):
        SudokuSolver.__init__(self, np.zeros((9, 9), int))
        self.nrandomsteps = nrandomsteps
        self.token = np.arange(10)
        
        
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
                counts = count_nonzero_unique(grid[i:i + 3, j:j + 3].flatten())
                if (counts > 1).any():
                    return False
        return True
            
        
    def random_grid(self):
        self.grid = np.zeros((9, 9), int)
        valid_steps = 0
        while valid_steps <= self.nrandomsteps:
            oldgrid = self.grid.copy()
            self.grid[np.random.randint(9), np.random.randint(9)] = np.random.randint(1, 10)
            is_solvable = False
            if self.is_valid(self.grid):
                with timeout(1):
                  self.solven(1)
                  valid_steps += 1
                  is_solvable = True
            if not is_solvable:
                self.grid = oldgrid
                valid_steps = self.nrandomsteps
        self.solven(1)
        self.random_seed = self.grid.copy()
        self.grid = self.solutions[0]
        return self.grid
    
    
    def randomize_token(self):
        np.random.shuffle(self.token[1:])
        return self.get_tokenized_grid()
        
    
    def get_tokenized_grid(self):
        return self.token[self.grid.flatten()].reshape(self.grid.shape)


