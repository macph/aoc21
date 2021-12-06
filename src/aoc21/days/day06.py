from importlib.resources import open_text
from typing import Iterable, List


class School:
    def __init__(self, initial: Iterable[int]):
        # Group all fish by their timers.
        self._timers: List[int] = [0] * 9
        for i in initial:
            self._timers[i] += 1

    @property
    def size(self) -> int:
        return sum(self._timers)

    def step(self, steps: int = 1):
        for _ in range(steps):
            self._step()

    def _step(self):
        timer_0 = self._timers[0]

        # Decrement timer if it is greater than zero.
        for i in range(1, 9):
            self._timers[i - 1] = self._timers[i]

        # Fish with timer 0 will spawn more fish with timer 8 and have their timers reset to 6.
        self._timers[6] += timer_0
        self._timers[8] = timer_0


def _get_school() -> School:
    with open_text("aoc21.days", "day06.txt") as f:
        # Expect one line.
        return School(map(int, f.readline().split(",")))


def part1() -> object:
    school = _get_school()
    school.step(80)

    return school.size


def part2() -> object:
    school = _get_school()
    school.step(256)

    return school.size
