from __future__ import print_function
import numpy as np


def get_sudoku_neighbor_list(dim=3, rank=2):
    """ Generate tge neighbor list for generic Sudoku problems.

    The neighbor list is the list of sudoku cells that the given cell
    is not supposed to share the same number.

    Each sub-tensor will have the shape of (dim, ) * rank and the total
    tensor will have the shape of (dim ** rank, ) * rank. In the trivial
    case, when dim=3 and rank=2, the matrix is 9x9 and the sub-matrix is
    3x3.
    """
    nnumbers = dim ** rank
    nneighbors = rank * (nnumbers - 1) + (nnumbers - 1 - (dim - 1) * rank)
    shape = (nnumbers, ) * rank
    subshape = (dim, ) * rank
    #
    neighbor_list = np.zeros(shape + (nneighbors, rank), int)
    #
    for tindex in np.ndindex(*shape):
        index = np.array(tindex)
        major_index = (index // dim) * dim
        nindex = 0
        #
        for j in range(rank):
            for i in range(nnumbers):
                if index[j] != i:
                    tmp = index.copy()
                    tmp[j] = i
                    neighbor_list[tindex + (nindex, slice(None))] = tmp
                    nindex += 1

        for sub_index in np.ndindex(*subshape):
            tmpindex = np.array(major_index) + np.array(sub_index)
            if np.count_nonzero(tmpindex != index) > 1:
                neighbor_list[tindex + (nindex, slice(None))] = tmpindex
                nindex += 1
        sortedorder = np.argsort(np.ravel_multi_index(neighbor_list[tindex].T, shape))
        neighbor_list[tindex] = neighbor_list[tindex][sortedorder]
    return neighbor_list


def _get_normal_sudoku_neighbor_list():
    neighbor_list = np.zeros((9, 9, 20, 2), int)
    for x in range(9):
        for y in range(9):
            x0 = (x // 3) * 3
            y0 = (y // 3) * 3
            index = 0
            for i in range(9):
                if i != y:
                    neighbor_list[x, y, index, :] = (x, i)
                    index += 1
                if i != x:
                    neighbor_list[x, y, index, :] = (i, y)
                    index += 1
            for i in range(3):
                for j in range(3):
                    if (x0 + i != x) and (y0 + j != y):
                        neighbor_list[x, y, index, :] = (x0 + i, y0 + j)
                        index += 1
            sortedorder = np.argsort(np.ravel_multi_index(neighbor_list[x, y].T, (9, 9)))
            neighbor_list[x, y] = neighbor_list[x, y][sortedorder]
    return neighbor_list


def _check_sudoku_neighbor_list():
    normal_sudoku_neighbor_list = _get_normal_sudoku_neighbor_list()
    sudoku_neighbor_list = get_sudoku_neighbor_list(dim=3, rank=2)
    assert np.array_equal(sudoku_neighbor_list, normal_sudoku_neighbor_list)


sudoku_neighbor_list = get_sudoku_neighbor_list(dim=3, rank=2)


if __name__ == "__main__":
    _check_sudoku_neighbor_list()

    nl = get_sudoku_neighbor_list(dim=2, rank=3)
    print(nl[0, 0, 0])
