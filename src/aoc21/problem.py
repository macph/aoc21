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
