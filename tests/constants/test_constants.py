import numpy as np

from sudoku.constants import _get_normal_sudoku_neighbor_list, get_sudoku_neighbor_list


def test_sudoku_neighbor_list():
    normal_sudoku_neighbor_list = _get_normal_sudoku_neighbor_list()
    sudoku_neighbor_list = get_sudoku_neighbor_list(dim=3, rank=2)
    assert np.array_equal(sudoku_neighbor_list, normal_sudoku_neighbor_list)


