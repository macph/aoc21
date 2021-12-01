from importlib.resources import open_text
from typing import Iterable, List

from more_itertools import windowed


def _get_measurements() -> List[int]:
    with open_text("aoc21.days", "day01.txt") as f:
        return [int(line.strip()) for line in f]


def _count_increases(data: Iterable[int]) -> int:
    return sum(1 for (i, j) in windowed(data, 2) if i < j)


def part1() -> object:
    return _count_increases(_get_measurements())


def part2() -> object:
    windows = map(sum, windowed(_get_measurements(), 3))
    return _count_increases(windows)
