from aoc21.days.day03 import find_gamma_epsilon, find_rating, Rating


NUMBERS = [
    0b00100,
    0b11110,
    0b10110,
    0b10111,
    0b10101,
    0b01111,
    0b00111,
    0b11100,
    0b10000,
    0b11001,
    0b00010,
    0b01010,
]


def test_gamma_epsilon():
    assert find_gamma_epsilon(NUMBERS) == (22, 9)


def test_oxygen_rating():
    assert find_rating(NUMBERS, Rating.OXYGEN) == 23


def test_carbon_dioxide_rating():
    assert find_rating(NUMBERS, Rating.CARBON_DIOXIDE) == 10
