from importlib.resources import open_text
from typing import Callable, Iterable, List, Tuple


def find_minimum_sum_distances(
    func: Callable[[Iterable[int], int], int], positions: Iterable[int]
) -> Tuple[int, int]:
    # Perform a ternary search.
    minimum = min(positions)
    maximum = max(positions)

    while minimum + 1 < maximum:
        third = round((maximum - minimum) / 3)
        lower = minimum + third
        upper = maximum - third

        if func(positions, lower) < func(positions, upper):
            # The minimum is closer to the lower point.
            maximum = upper
        else:
            # The minimum point is closer to the upper point.
            minimum = lower

    return minimum, func(positions, minimum)


def sum_constant(values: Iterable[int], value: int) -> int:
    return sum(abs(v - value) for v in values)


def sum_increasing(values: Iterable[int], value: int) -> int:
    return sum(_triangular(abs(v - value)) for v in values)


def _triangular(x: int) -> int:
    return x * (x + 1) // 2


def _get_positions() -> List[int]:
    with open_text("aoc21.days", "day07.txt") as f:
        # Expect all numbers on a single line.
        return list(map(int, f.readline().split(",")))


def part1() -> object:
    _, required = find_minimum_sum_distances(sum_constant, _get_positions())

    return required


def part2() -> object:
    _, required = find_minimum_sum_distances(sum_increasing, _get_positions())

    return required
