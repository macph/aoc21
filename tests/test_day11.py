from copy import copy

from aoc21.days.day11 import OctopusGrid, Point


def test_point_add():
    assert Point(15, 10) + Point(-5, 10) == Point(10, 20)


GRID = OctopusGrid(
    [
        [5, 4, 8, 3, 1, 4, 3, 2, 2, 3],
        [2, 7, 4, 5, 8, 5, 4, 7, 1, 1],
        [5, 2, 6, 4, 5, 5, 6, 1, 7, 3],
        [6, 1, 4, 1, 3, 3, 6, 1, 4, 6],
        [6, 3, 5, 7, 3, 8, 5, 4, 7, 8],
        [4, 1, 6, 7, 5, 2, 4, 6, 4, 5],
        [2, 1, 7, 6, 8, 4, 1, 7, 2, 1],
        [6, 8, 8, 2, 8, 8, 1, 1, 3, 4],
        [4, 8, 4, 6, 8, 4, 8, 5, 5, 4],
        [5, 2, 8, 3, 7, 5, 1, 5, 2, 6],
    ]
)


def test_octopus_grid_step():
    grid = copy(GRID)
    assert grid.step_once() == 0
    assert grid.step_once() == 35
    assert grid.step_once() == 45
    assert grid.step_once() == 16
    assert grid.step_once() == 8
    assert grid.step_once() == 1
    assert grid.step_once() == 7
    assert grid.step_once() == 24
    assert grid.step_once() == 39
    assert grid.step_once() == 29


def test_octopus_grid_multiple_steps():
    grid = copy(GRID)
    assert grid.step(10) == 204
