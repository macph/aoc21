import pytest

from aoc21.days.day08 import Entry, Segment


@pytest.mark.parametrize(
    "string, expected",
    [
        ("a", Segment.A),
        ("ac", Segment.A | Segment.C),
        ("acf", Segment.A | Segment.C | Segment.F),
        ("abcdefg", Segment(127)),
    ],
)
def test_parse_segment(string, expected):
    assert Segment.parse(string) == expected


@pytest.mark.parametrize(
    "segment, expected",
    [
        (Segment.A, 1),
        (Segment.A | Segment.C, 2),
        (Segment.A | Segment.C | Segment.F, 3),
        (Segment(127), 7),
    ],
)
def test_segment_length(segment, expected):
    assert len(segment) == expected


@pytest.mark.parametrize(
    "segment, expected",
    [
        (Segment.A, [Segment.A]),
        (Segment.A | Segment.C, [Segment.A, Segment.C]),
        (Segment.A | Segment.C | Segment.F, [Segment.A, Segment.C, Segment.F]),
        (Segment(127), list(Segment)),
    ],
)
def test_segment_iter(segment, expected):
    assert list(segment) == expected


ENTRY_INPUT = (
    "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | "
    "cdfeb fcadb cdfeb cdbaf"
)
ENTRY = Entry(
    [
        Segment(127),
        Segment(62),
        Segment(109),
        Segment(47),
        Segment(11),
        Segment(63),
        Segment(126),
        Segment(51),
        Segment(95),
        Segment(3),
    ],
    [
        Segment(62),
        Segment(47),
        Segment(62),
        Segment(47),
    ],
)


def test_parse_entry():
    entry = Entry.parse(ENTRY_INPUT)
    assert entry.signals == ENTRY.signals
    assert entry.digits == ENTRY.digits


def test_entry_find_digits():
    assert ENTRY.find_digits() == {
        Segment(127): 8,
        Segment(62): 5,
        Segment(109): 2,
        Segment(47): 3,
        Segment(11): 7,
        Segment(63): 9,
        Segment(126): 6,
        Segment(51): 4,
        Segment(95): 0,
        Segment(3): 1,
    }


def test_entry_decode():
    assert ENTRY.decode() == 5353
