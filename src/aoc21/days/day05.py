from collections import Counter
from importlib.resources import open_text
from typing import NamedTuple, Iterable, List


class Position(NamedTuple):
    x: int
    y: int

    @classmethod
    def parse(cls, s: str) -> "Position":
        try:
            x, y = map(int, s.split(",", 1))
        except ValueError as e:
            raise ValueError("Expected two integers separated by a comma.") from e

        return cls(x, y)


class Line(NamedTuple):
    start: Position
    end: Position

    @classmethod
    def parse(cls, s: str) -> "Line":
        try:
            start, end = map(Position.parse, s.split("->", 1))
        except ValueError as e:
            raise ValueError("Expected two coordinates separated by a '->'.") from e

        return cls(start, end)

    def horizontal(self) -> int:
        return abs(self.end.x - self.start.x)

    def vertical(self) -> int:
        return abs(self.end.y - self.start.y)

    def is_horizontal_or_vertical(self) -> bool:
        return self.horizontal() == 0 or self.vertical() == 0

    def positions(self) -> Iterable[Position]:
        x, y = self.horizontal(), self.vertical()
        if x == 0:
            return (
                Position(self.start.x, y)
                for y in _inclusive_range(self.start.y, self.end.y)
            )
        elif y == 0:
            return (
                Position(x, self.start.y)
                for x in _inclusive_range(self.start.x, self.end.x)
            )
        elif x == y:
            return (
                Position(x, y)
                for x, y in zip(
                    _inclusive_range(self.start.x, self.end.x),
                    _inclusive_range(self.start.y, self.end.y),
                )
            )
        else:
            raise ValueError("Lines must be horizontal, vertical or diagonal.")


def _inclusive_range(start: int, end: int) -> Iterable[int]:
    if start <= end:
        return range(start, end + 1)
    else:
        return range(start, end - 1, -1)


def _get_data() -> List[Line]:
    with open_text("aoc21.days", "day05.txt") as f:
        return list(map(Line.parse, f))


def _count_overlaps(lines: Iterable[Line]) -> int:
    occupied = Counter()
    for line in lines:
        occupied.update(line.positions())

    return sum(1 for c in occupied.values() if c > 1)


def part1() -> object:
    return _count_overlaps(filter(Line.is_horizontal_or_vertical, _get_data()))


def part2() -> object:
    return _count_overlaps(_get_data())
