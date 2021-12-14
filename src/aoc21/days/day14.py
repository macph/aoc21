from collections import Counter
from importlib.resources import open_text
from typing import Dict, Iterable, NamedTuple, Tuple

from more_itertools import windowed


class Pair(NamedTuple):
    left: str
    right: str


class Rule(NamedTuple):
    left: str
    right: str
    inner: str

    @classmethod
    def parse(cls, s: str) -> "Rule":
        split = list(map(str.strip, s.split("->")))

        if len(split) != 2 or len(split[0]) != 2 or len(split[1]) != 1:
            raise ValueError("Expected rule in form 'AB -> C'.")

        left = split[0][0]
        right = split[0][1]
        inner = split[1]

        return cls(left, right, inner)

    @property
    def pair(self) -> Pair:
        return Pair(self.left, self.right)

    @property
    def left_pair(self) -> Pair:
        return Pair(self.left, self.inner)

    @property
    def right_pair(self) -> Pair:
        return Pair(self.inner, self.right)


class RuleSet:
    def __init__(self, rules: Iterable[Rule]):
        self._rules: Dict[Pair] = {r.pair: r for r in rules}

    def apply_with_count(self, template: str, steps: int) -> Counter[str]:
        if len(template) < 2:
            raise ValueError("Expected template with length at least 2.")

        # We're not interested in the actual sequence of characters, only their counts.
        # Use a counter to store counts for each pair in the sequence and add them as
        # the sequence is expanded.
        counted_pairs: Counter[Pair] = Counter(Pair(*w) for w in windowed(template, 2))

        for _ in range(steps):
            counted_pairs = self._apply_with_count(counted_pairs)

        counted: Counter[str] = Counter()
        for pair, count in counted_pairs.items():
            counted[pair.left] += count

        # We've only added the counts for the starting character in each pair, which
        # does not include the final character.
        counted[template[-1]] += 1

        return counted

    def _apply_with_count(self, counted: Counter[Pair]) -> Counter[Pair]:
        new: Counter[Pair] = Counter()

        for pair, count in counted.items():
            rule = self._rules[pair]
            new[rule.left_pair] += count
            new[rule.right_pair] += count

        return new


def _read_template_and_rules() -> Tuple[str, RuleSet]:
    with open_text("aoc21.days", "day14.txt") as f:
        lines = iter(f)

        # Expect template on first line.
        template = next(lines).strip()

        # Expect an empty line after template.
        next(lines)

        # Rest of lines are the insertion rules.
        rules = RuleSet(map(Rule.parse, lines))

        return template, rules


def part1() -> object:
    template, rules = _read_template_and_rules()
    counted = rules.apply_with_count(template, 10)

    return max(counted.values()) - min(counted.values())


def part2() -> object:
    template, rules = _read_template_and_rules()
    counted = rules.apply_with_count(template, 40)

    return max(counted.values()) - min(counted.values())
