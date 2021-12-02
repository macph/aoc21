from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Problem:
    """
    Represents a problem to be solved.
    """

    day: int
    part: int
    solver: Callable[[], object]


@dataclass
class Solution:
    """
    Represents a solution to a problem.
    """

    problem: Problem
    value: object
    exception: Optional[Exception]
    elapsed_s: float
    runs: int

    @property
    def elapsed(self) -> str:
        return _format_elapsed(self.elapsed_s)


def _format_elapsed(seconds: float) -> str:
    if seconds >= 10.0:
        return f"{seconds:.1f} s"
    elif seconds >= 1e-2:
        milliseconds = seconds * 1e3
        return f"{milliseconds:.1f} ms"
    elif seconds >= 1e-5:
        microseconds = seconds * 1e6
        return f"{microseconds:.1f} µs"
    else:
        nanoseconds = seconds * 1e9
        return f"{nanoseconds:.1f} ns"
