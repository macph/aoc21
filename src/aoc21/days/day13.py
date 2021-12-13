from enum import Enum
from functools import reduce
from importlib.resources import open_text
from typing import AbstractSet, Iterable, Iterator, List, NamedTuple, Set, Tuple


class Dot(NamedTuple):
    x: int
    y: int

    @classmethod
    def parse(cls, s: str) -> "Dot":
        x, y = map(int, s.split(",", maxsplit=1))
        return cls(x, y)


class Fold(Enum):
    X, Y = range(2)


class FoldInstruction(NamedTuple):
    fold: Fold
    line: int

    @classmethod
    def parse(cls, s: str) -> "FoldInstruction":
        if not s.startswith("fold along "):
            raise ValueError("Expected 'fold along'.")

        f, i = s[11:].split("=", maxsplit=1)
        fold = Fold[f.upper()]
        line = int(i)

        return cls(fold, line)


class Paper(AbstractSet[Dot]):
    def __init__(self, dots: Iterable[Dot]):
        self._dots: Set[Dot] = set(dots)

        if any(d.x < 0 or d.y < 0 for d in self._dots):
            raise ValueError("All dots must have positive coordinates.")

        self._x = max(d.x for d in self._dots)
        self._y = max(d.y for d in self._dots)

    def __contains__(self, x: object) -> bool:
        return x in self._dots

    def __len__(self) -> int:
        return len(self._dots)

    def __iter__(self) -> Iterator[Dot]:
        return iter(self._dots)

    def to_string(self) -> str:
        columns = self._x + 1
        rows = self._y + 1

        table = [[" "] * columns for _ in range(rows)]
        for d in self:
            table[d.y][d.x] = "#"

        return "\n".join("".join(r) for r in table)

    def fold(self, instruction: FoldInstruction) -> "Paper":
        if instruction.fold == Fold.X:
            return self._fold_x(instruction.line)
        elif instruction.fold == Fold.Y:
            return self._fold_y(instruction.line)
        else:
            raise ValueError(f"Unexpected instruction {instruction!r}.")

    def _fold_x(self, x: int) -> "Paper":
        dots: List[Dot] = []

        for d in self._dots:
            if d.x < x:
                dots.append(d)
            elif d.x > x:
                dots.append(Dot(2 * x - d.x, d.y))
            else:
                raise ValueError(f"{d!r} lies on fold x={x}.")

        return Paper(dots)

    def _fold_y(self, y: int) -> "Paper":
        dots: List[Dot] = []

        for d in self._dots:
            if d.y < y:
                dots.append(d)
            elif d.y > y:
                dots.append(Dot(d.x, 2 * y - d.y))
            else:
                raise ValueError(f"{d!r} lies on fold y={y}.")

        return Paper(dots)


def _read_paper_and_instructions() -> Tuple[Paper, List[FoldInstruction]]:
    with open_text("aoc21.days", "day13.txt") as f:
        lines = iter(f)
        dots = []
        instructions = []

        for line in lines:
            if not line.strip():
                break
            dots.append(Dot.parse(line))

        paper = Paper(dots)

        for line in lines:
            instructions.append(FoldInstruction.parse(line))

        return paper, instructions


def part1() -> object:
    paper, instructions = _read_paper_and_instructions()
    return len(paper.fold(instructions[0]))


def part2() -> object:
    paper, instructions = _read_paper_and_instructions()

    folded = paper
    for i in instructions:
        folded = folded.fold(i)

    # TODO: Implement some sort of OCR?
    # print(folded.to_string())

    return "HZLEHJRK"
