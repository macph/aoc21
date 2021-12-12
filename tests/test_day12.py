import pytest

from aoc21.days.day12 import Cavern


CAVERN_1 = Cavern(
    [
        ("start", "A"),
        ("start", "b"),
        ("A", "c"),
        ("A", "b"),
        ("b", "d"),
        ("A", "end"),
        ("b", "end"),
    ]
)

CAVERN_2 = Cavern(
    [
        ("dc", "end"),
        ("HN", "start"),
        ("start", "kj"),
        ("dc", "start"),
        ("dc", "HN"),
        ("LN", "dc"),
        ("HN", "end"),
        ("kj", "sa"),
        ("kj", "HN"),
        ("kj", "dc"),
    ]
)

CAVERN_3 = Cavern(
    [
        ("fs", "end"),
        ("he", "DX"),
        ("fs", "he"),
        ("start", "DX"),
        ("pj", "DX"),
        ("end", "zg"),
        ("zg", "sl"),
        ("zg", "pj"),
        ("pj", "he"),
        ("RW", "he"),
        ("fs", "DX"),
        ("pj", "RW"),
        ("zg", "RW"),
        ("start", "pj"),
        ("he", "WI"),
        ("zg", "he"),
        ("pj", "fs"),
        ("start", "RW"),
    ]
)


@pytest.mark.parametrize(
    "cavern, visit_once, count",
    [
        (CAVERN_1, True, 10),
        (CAVERN_1, False, 36),
        (CAVERN_2, True, 19),
        (CAVERN_2, False, 103),
        (CAVERN_3, True, 226),
        (CAVERN_3, False, 3509),
    ],
)
def test_cavern_count_paths(cavern, visit_once, count):
    assert cavern.count_paths(visit_once) == count
