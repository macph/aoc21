from aoc21.days.day07 import (
    find_minimum_sum_distances,
    sum_constant,
    sum_increasing,
)


def test_minimum_sum_constant_distances():
    positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    assert find_minimum_sum_distances(sum_constant, positions) == (2, 37)


def test_minimum_sum_increasing_distances():
    positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    assert find_minimum_sum_distances(sum_increasing, positions) == (5, 168)
