from importlib.resources import open_text
from itertools import chain
from math import isqrt
from typing import Iterable, List, NamedTuple, Sequence


class BoardScore(NamedTuple):
    index: int
    score: int


class Board:
    def __init__(self, grid: Iterable[int]):
        self._grid: List[int] = list(grid)
        self._size: int = len(self._grid)
        self._side: int = isqrt(self._size)

        if self._side ** 2 != self._size:
            raise ValueError("The grid must be a square.")

    def row(self, index: int) -> Iterable[int]:
        if not 0 <= index < self._side:
            raise ValueError("Row index outside bounds.")

        start = index * self._side
        end = start + self._side

        return (self._grid[i] for i in range(start, end))

    def column(self, index: int) -> Iterable[int]:
        if not 0 <= index < self._side:
            raise ValueError("Column index outside bounds.")

        return (self._grid[i] for i in range(index, self._size, self._side))

    def draw_until_complete(self, numbers: Iterable[int]) -> BoardScore:
        # Collect numbers into row and column sets.
        rows = [set(self.row(i)) for i in range(self._side)]
        columns = [set(self.column(i)) for i in range(self._side)]

        i = 0

        for n in numbers:
            # Remove number from rows and columns if it exists.
            for r in rows:
                r.discard(n)
            for c in columns:
                c.discard(n)

            if not all(rows) or not all(columns):
                # Stop once a row or column has been emptied. Calculate the score as
                # the sum of unmarked numbers multiplied by the final number.
                score = sum(chain.from_iterable(rows)) * n
                return BoardScore(i, score)

            i += 1

        return BoardScore(i, 0)


class BoardGame(NamedTuple):
    numbers: Sequence[int]
    boards: Sequence[Board]

    def first_game_to_win(self) -> BoardScore:
        # Get the board score with the smallest index.
        return min(map(self._draw_until_complete, self.boards))

    def last_game_to_win(self) -> BoardScore:
        # Get the board score with the largest index.
        return max(map(self._draw_until_complete, self.boards))

    def _draw_until_complete(self, board: Board) -> BoardScore:
        return board.draw_until_complete(self.numbers)


def _split_on_empty(iterable: Iterable[str]) -> Iterable[Sequence[str]]:
    iterator = iter(iterable)

    while True:
        sequence = []

        for value in iterator:
            if value:
                sequence.append(value)
            else:
                # Ran into empty string; continue after yielding sequence.
                yield sequence
                break
        else:
            # Iterator has been exhausted; stop after yielding sequence.
            yield sequence
            return


def _create_board(group: Sequence[str]) -> Board:
    integers = map(int, chain.from_iterable(map(str.split, group)))
    return Board(integers)


def _create_board_game() -> BoardGame:
    with open_text("aoc21.days", "day04.txt") as f:
        lines = map(str.strip, f)

        # Read the first line as a sequence of integers separated by commas.
        numbers = list(map(int, next(lines).split(",")))
        # Skip the next line, which is expected to be empty.
        next(lines)

        # Read the rest of lines as boards, separated by empty lines.
        boards = list(map(_create_board, _split_on_empty(lines)))

        return BoardGame(numbers, boards)


def part1() -> object:
    return _create_board_game().first_game_to_win().score


def part2() -> object:
    return _create_board_game().last_game_to_win().score
