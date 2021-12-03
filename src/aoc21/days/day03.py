from enum import Enum
from importlib.resources import open_text
from math import floor, log2
from typing import Sequence, Tuple, List


class Rating(Enum):
    OXYGEN, CARBON_DIOXIDE = range(2)


def _number_of_bits(number: int) -> int:
    if number > 0:
        return floor(log2(number)) + 1
    else:
        raise ValueError("Number must be positive.")


def _flip_bits(bits: int, number: int) -> int:
    return ~number & (1 << bits) - 1


def find_gamma_epsilon(numbers: Sequence[int]) -> Tuple[int, int]:
    half_count = len(numbers) / 2
    bits = max(map(_number_of_bits, numbers))
    bits_set = [0] * bits

    for number in numbers:
        for i in range(bits):
            if number & (1 << i) > 0:
                bits_set[i] += 1

    gamma = 0
    for i, bit_count in enumerate(bits_set):
        if bit_count >= half_count:
            gamma |= 1 << i

    epsilon = _flip_bits(bits, gamma)

    return gamma, epsilon


def find_rating(numbers: Sequence[int], rating: Rating) -> int:
    remaining = list(numbers)
    # Match with the gamma rate (index 0) if calculating the oxygen generator rating,
    # otherwise match with the epsilon rate (index 1) for the CO2 scrubber rating.
    index = rating.value
    # Start comparing with the most significant bit and decrement each time.
    offset = max(map(_number_of_bits, numbers)) - 1

    while len(remaining) > 1 and offset > -1:
        criteria = find_gamma_epsilon(remaining)[index]
        bit = 1 << offset
        bit_criteria = criteria & bit

        # Work through the list backwards when deleting items.
        for i in range(len(remaining) - 1, -1, -1):
            if remaining[i] & bit != bit_criteria:
                del remaining[i]

        offset -= 1

    if len(remaining) != 1:
        raise ValueError(f"Expected a single value, got {len(remaining)}.")

    return remaining[0]


def _get_binary_numbers() -> List[int]:
    with open_text("aoc21.days", "day03.txt") as f:
        return [int(line.strip(), 2) for line in f]


def part1() -> object:
    numbers = _get_binary_numbers()
    gamma, epsilon = find_gamma_epsilon(numbers)

    return gamma * epsilon


def part2() -> object:
    numbers = _get_binary_numbers()
    oxygen = find_rating(numbers, Rating.OXYGEN)
    carbon_dioxide = find_rating(numbers, Rating.CARBON_DIOXIDE)

    return oxygen * carbon_dioxide
