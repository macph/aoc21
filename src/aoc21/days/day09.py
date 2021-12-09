from collections import deque
from importlib.resources import open_text
from itertools import islice
from typing import Iterable, Mapping, Iterator, NamedTuple, Set, Deque, List


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class HeightMap(Mapping[Point, int]):
    _ADJACENT = [
        Point(-1, 0),
        Point(1, 0),
        Point(0, -1),
        Point(0, 1),
    ]

    def __init__(self, heights: Iterable[Iterable[int]]):
        self._map: List[List[int]] = list(map(list, heights))
        self._width = len(self._map[0])
        self._height = len(self._map)

        if not all(len(r) == self._width for r in self._map):
            raise ValueError("Expected all rows to have the same width.")

    def __getitem__(self, k: Point) -> int:
        return self._map[k.y][k.x]

    def __len__(self) -> int:
        return self._width * self._height

    def __iter__(self) -> Iterator[Point]:
        return (Point(i, j) for j in range(self._height) for i in range(self._width))

    @classmethod
    def parse(cls, s: str) -> "HeightMap":
        return cls(map(cls._parse_row, s.splitlines()))

    @staticmethod
    def _parse_row(row: str) -> Iterable[int]:
        return map(int, row)

    def get_risk_level(self, point: Point) -> int:
        return 1 + self[point]

    def find_basins(self) -> Iterable[Set[Point]]:
        return map(self._find_basin, self.find_low_points())

    def find_low_points(self) -> Iterable[Point]:
        return filter(self._is_low_point, self)

    def get_adjacent_points(self, point: Point) -> Iterable[Point]:
        if not self._within_bounds(point):
            raise ValueError(f"{point!r} not within map.")

        for a in self._ADJACENT:
            if self._within_bounds(adjacent := point + a):
                yield adjacent

    def _within_bounds(self, point: Point) -> bool:
        return 0 <= point.x < self._width and 0 <= point.y < self._height

    def _is_low_point(self, point: Point):
        height = self[point]
        return all(height < self[a] for a in self.get_adjacent_points(point))

    def _find_basin(self, low_point: Point) -> Set[Point]:
        found: Set[Point] = set()
        queue: Deque[Point] = deque()

        found.add(low_point)
        queue.append(low_point)

        while queue:
            point = queue.popleft()
            for adjacent in self.get_adjacent_points(point):
                if self[adjacent] < 9 and adjacent not in found:
                    found.add(adjacent)
                    queue.append(adjacent)

        return found


def _get_heightmap() -> HeightMap:
    with open_text("aoc21.days", "day09.txt") as f:
        return HeightMap.parse(f.read())


def _product(numbers: Iterable[int]) -> int:
    product = 1
    for n in numbers:
        product *= n

    return product


def part1() -> object:
    height_map = _get_heightmap()
    return sum(map(height_map.get_risk_level, height_map.find_low_points()))


def part2() -> object:
    height_map = _get_heightmap()
    basins = sorted(height_map.find_basins(), key=len, reverse=True)
    return _product(map(len, islice(basins, 3)))
