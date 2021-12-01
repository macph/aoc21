from dataclasses import dataclass
from time import perf_counter_ns
from typing import Callable


@dataclass
class Problem:
    """
    Represents a problem to be solved.
    """

    day: int
    part: int
    solver: Callable[[], object]

    def solve(self) -> "Solution":
        start = perf_counter_ns()
        solution = self.solver()
        end = perf_counter_ns()

        return Solution(self, solution, end - start)


@dataclass
class Solution:
    """
    Represents a solution to a problem.
    """

    problem: Problem
    solution: object
    elapsed_ns: int

    @property
    def elapsed(self) -> str:
        return _format_elapsed(self.elapsed_ns)


def _format_elapsed(nanoseconds: int) -> str:
    if nanoseconds < 10_000:
        return f"{nanoseconds} ns"
    elif nanoseconds < 10_000_000:
        microseconds = nanoseconds / 1000
        return f"{microseconds:.1f} µs"
    elif nanoseconds < 10_000_000_000:
        milliseconds = nanoseconds / 1_000_000
        return f"{milliseconds:.1f} ms"
    else:
        seconds = nanoseconds / 1_000_000_000
        return f"{seconds:.1f} s"
