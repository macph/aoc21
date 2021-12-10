from collections import deque
from dataclasses import dataclass
from importlib.resources import open_text
from typing import Deque, Iterable, List, Optional


PAIRS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

ILLEGAL_SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

INCOMPLETE_SCORES = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


@dataclass
class ParseResult:
    illegal: Optional[str]
    incomplete: Iterable[str]

    def is_valid(self) -> bool:
        return self.illegal is None

    def get_illegal_score(self) -> int:
        return ILLEGAL_SCORES.get(self.illegal, 0)

    def complete(self) -> int:
        score = 0
        for c in self.incomplete:
            score *= 5
            score += INCOMPLETE_SCORES[c]

        return score


def _parse_chunks(s: str) -> ParseResult:
    stack: Deque[str] = deque()
    illegal: Optional[str] = None

    for c in s:
        if c in "([{<":
            # Append opening character.
            stack.append(c)
        elif not stack or c != PAIRS[stack.pop()]:
            # No more opening characters or the closing character does not match last
            # opening character.
            illegal = c
            break

    incomplete = list(reversed(stack))

    return ParseResult(illegal, incomplete)


def _median(integers: Iterable[int]) -> int:
    ordered = sorted(integers)
    assert len(ordered) % 2 == 1
    return ordered[len(ordered) // 2]


def _read_chunks() -> List[str]:
    with open_text("aoc21.days", "day10.txt") as f:
        return list(map(str.strip, f))


def _parse_all_chunks() -> List[ParseResult]:
    return map(_parse_chunks, _read_chunks())


def part1() -> object:
    return sum(map(ParseResult.get_illegal_score, _parse_all_chunks()))


def part2() -> object:
    return _median(
        map(ParseResult.complete, filter(ParseResult.is_valid, _parse_all_chunks()))
    )
