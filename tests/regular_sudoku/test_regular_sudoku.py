import numpy as np

from sudoku.regular_sudoku import RegularSudoku

def test_solve_sudoku():
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
    s = RegularSudoku()
    s.set_grid(grid)
    s.solve()
    print(s.possibility_map())
    print(s.solutions)
    print(s.solutions_depth)
    assert s.grid_is_valid
    assert s.grid_is_solvable
    assert s.grid_is_solution_unique

    nonzero_x, nonzero_y = s.grid.nonzero()
    print("nonzero_x", nonzero_x)
    print("nonzero_y", nonzero_y)
    single_x, single_y = (s.possibility_map() == 1).nonzero()
    print("single_x", single_x)
    print("single_y", single_y)
    print(grid[tuple(s.neighbor_list[4, 4].T)].nonzero()[0])
    print()
    print("remove x, remove y, grid solvable, grid solution unique, possibility > 1, solutions depth")
    for i, j in s.neighbor_list[4, 4][grid[tuple(s.neighbor_list[4, 4].T)].nonzero()[0], :]:
        sprime = s.copy()
        sprime.grid[i, j] = 0
        print(i, j, sprime.grid_is_solvable, sprime.grid_is_solution_unique, sprime.possibility_map()[4, 4] > 1, sprime.solutions_depth)

def test_random_generate_sudoku():
    s = RegularSudoku()
    s.random_grid()
    print(s.grid)
    print(s.seed_grid)
    assert s.grid_is_solvable
