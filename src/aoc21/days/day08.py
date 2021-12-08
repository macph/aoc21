from dataclasses import dataclass
from enum import Flag
from importlib.resources import open_text
from itertools import islice
from typing import Dict, List, Mapping


class Segment(Flag):
    A, B, C, D, E, F, G = 1, 2, 4, 8, 16, 32, 64

    @classmethod
    def parse(cls, s: str) -> "Segment":
        value = 0
        for c in s.upper():
            value |= cls[c].value

        return cls(value)

    def __len__(self) -> int:
        return bin(self.value).count("1")

    def __iter__(self):
        return (s for s in self.__class__ if s in self)


@dataclass
class Entry:
    signals: List[Segment]
    digits: List[Segment]

    @classmethod
    def parse(cls, s: str) -> "Entry":
        words = s.split()
        if len(words) != 15 or words[10] != "|":
            raise ValueError("Expected 10 signal patterns followed by 4 digits.")

        # Parse 10 words as segments, the '|' separator and 4 words as segments.
        iterator = iter(words)
        signals = list(map(Segment.parse, islice(iterator, 10)))
        digits = list(map(Segment.parse, islice(iterator, 1, None)))

        return cls(signals, digits)

    def decode(self) -> int:
        digits = self.find_digits()

        # Use the mapping to decode the digits and combine them into an integer.
        value = 0
        length = len(self.digits)
        for i in range(length):
            value += 10 ** (length - i - 1) * digits[self.digits[i]]

        return value

    def find_digits(self) -> Mapping[Segment, int]:
        # Start by creating maps for digits and segments.
        digits: Dict[int, Segment] = {}
        mapping: Dict[Segment, Segment] = {}

        # Find 2 as it is the only digit not to contain segment F.
        for f in Segment:
            found = [s for s in self.signals if f not in s]
            if len(found) == 1:
                digits[2] = found[0]
                mapping[Segment.F] = f
                break
        else:
            raise ValueError("Cannot find segment F.")

        # Find 7 (three segments) and 1 (two segments); we can find segment A.
        digits[1] = next(s for s in self.signals if len(s) == 2)
        digits[7] = next(s for s in self.signals if len(s) == 3)
        mapping[Segment.A] = digits[1] ^ digits[7]

        # Deduce segment C from 1.
        mapping[Segment.C] = digits[1] ^ mapping[Segment.F]

        # Find 6 by removing C from 8.
        digits[8] = next(s for s in self.signals if len(s) == 7)
        digits[6] = digits[8] ^ mapping[Segment.C]

        # Find 5 which differs from 6 with segment E removed.
        for e in digits[6]:
            five = digits[6] ^ e
            if five in self.signals:
                digits[5] = five
                mapping[Segment.E] = e
                break
        else:
            raise ValueError("Cannot find segment E.")

        # Find 9 which differs from 8 with segment E removed.
        digits[9] = digits[8] ^ mapping[Segment.E]

        # Find 4 (four segments).
        digits[4] = next(s for s in self.signals if len(s) == 4)

        # Find segment G by adding segment A to 4 then compare with 9.
        mapping[Segment.G] = digits[9] ^ (digits[4] | mapping[Segment.A])

        # Find segment B and D by using the difference of 1 and 4 and remove either
        # from 9 to find 3.
        b_d = digits[1] ^ digits[4]
        for b in b_d:
            three = digits[9] ^ b
            if three in self.signals:
                digits[3] = three
                mapping[Segment.B] = b
                mapping[Segment.D] = b_d ^ b
                break
        else:
            raise ValueError("Cannot find segment B.")

        # Find 0 by removing D from 8.
        digits[0] = digits[8] ^ mapping[Segment.D]

        # Finally, flip the digits mapping and return it.
        return {s: d for d, s in digits.items()}


def _get_entries() -> List[Entry]:
    with open_text("aoc21.days", "day08.txt") as f:
        return list(map(Entry.parse, f))


def part1() -> object:
    # The digits 1, 4, 7 and 8 have 2, 4, 3 and 7 segments respectively.
    unique = (2, 3, 4, 7)
    return sum(1 for e in _get_entries() for d in e.digits if len(d) in unique)


def part2() -> object:
    return sum(map(Entry.decode, _get_entries()))
