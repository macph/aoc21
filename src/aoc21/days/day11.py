from collections import deque
from importlib.resources import open_text
from itertools import count
from typing import NamedTuple, Iterable, List, Iterator, Mapping, Set, Deque


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class OctopusGrid(Mapping[Point, int]):
    _ADJACENT = [
        Point(-1, -1),
        Point(0, -1),
        Point(1, -1),
        Point(-1, 0),
        Point(1, 0),
        Point(-1, 1),
        Point(0, 1),
        Point(1, 1),
    ]

    def __init__(self, octopuses: Iterable[Iterable[int]]):
        self._grid: List[List[int]] = list(map(list, octopuses))
        self._height: int = len(self._grid)
        self._width: int = len(self._grid[0])

        if not all(len(r) == self._width for r in self._grid):
            raise ValueError("Expected all rows to have the same width.")

    def __getitem__(self, k: Point) -> int:
        if self._within_bounds(k):
            return self._grid[k.y][k.x]
        else:
            raise KeyError(k)

    def __len__(self) -> int:
        return self._width * self._height

    def __iter__(self) -> Iterator[Point]:
        return (Point(i, j) for j in range(self._height) for i in range(self._width))

    def __copy__(self):
        return self.__class__(self._grid)

    def step(self, steps: int) -> int:
        return sum(self.step_once() for _ in range(steps))

    def step_until_all_flash(self) -> int:
        size = len(self)
        for i in count(1):
            if self.step_once() == size:
                return i

    def step_once(self) -> int:
        points: List[Point] = list(self)
        queue: Deque[Point] = deque()

        for p in points:
            if self._increment_level(p):
                queue.appendleft(p)

        while queue:
            p = queue.pop()
            for a in self._find_adjacent(p):
                if self._increment_level(a):
                    queue.appendleft(a)

        flashes = 0
        for p in points:
            if self[p] > 9:
                flashes += 1
                self._reset_level(p)

        return flashes

    def _within_bounds(self, point: Point) -> bool:
        return 0 <= point.x < self._width and 0 <= point.y < self._height

    def _find_adjacent(self, point: Point) -> Iterable[Point]:
        assert self._within_bounds(point)
        for a in self._ADJACENT:
            p = point + a
            if self._within_bounds(p):
                yield p

    def _increment_level(self, point: Point) -> bool:
        assert self._within_bounds(point)

        level = self._grid[point.y][point.x]
        if level > 10:
            return False

        self._grid[point.y][point.x] = level + 1
        return level == 9

    def _reset_level(self, point: Point):
        assert self._within_bounds(point)
        self._grid[point.y][point.x] = 0


def _read_row(s: str) -> Iterable[int]:
    return map(int, s.strip())


def _read_grid() -> OctopusGrid:
    with open_text("aoc21.days", "day11.txt") as f:
        return OctopusGrid(map(_read_row, f))


def part1() -> object:
    return _read_grid().step(100)


def part2() -> object:
    return _read_grid().step_until_all_flash()
