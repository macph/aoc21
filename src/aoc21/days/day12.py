from collections import defaultdict, Counter
from importlib.resources import open_text
from itertools import chain
from typing import (
    Tuple,
    Iterable,
    Set,
    DefaultDict,
    Sequence,
    Dict,
    NamedTuple,
    Optional,
)


class Visited(NamedTuple):
    last: str
    visit_once: bool
    small_caves: Tuple[str, ...]

    @classmethod
    def from_path(cls, path: Sequence[str], visit_once: bool) -> Optional["Visited"]:
        last = path[-1]
        # Sort all small caves so the hash will be order-invariant.
        small_caves = tuple(sorted(c for c in path if c != "start" and c.islower()))

        # Check the small caves being visited.
        visited_twice = None
        for cave, count in Counter(small_caves).items():
            if count == 1:
                continue
            elif visit_once:
                # Small caves cannot be visited more than once if 'visit_once' is set.
                return None
            elif count > 2:
                # Small caves cannot be visited more than twice.
                return None
            elif visited_twice is not None:
                # Only one small cave can be visited twice if 'visit_once' is not set.
                return None
            else:
                visited_twice = cave

        return cls(last, visit_once, small_caves)

    def append(self, cave: str) -> Optional["Visited"]:
        # The original path is not required; only the small caves and the last cave
        # matter.
        path = list(chain(self.small_caves, (cave,)))
        return self.from_path(path, self.visit_once)


class Cavern:
    def __init__(self, connections: Iterable[Tuple[str, str]]):
        self._connections: DefaultDict[str, Set[str]] = defaultdict(set)

        # Set up graph with bidirectional edges.
        for start, end in connections:
            self._connections[start].add(end)
            self._connections[end].add(start)

    def count_paths(self, visit_once: bool) -> int:
        first = Visited.from_path(["start"], visit_once)
        return self._count_paths(first, {})

    def _count_paths(self, visited: Visited, cache: Dict[Visited, int]) -> int:
        found = cache.get(visited)
        if found is not None:
            # Already found all paths starting in this cave.
            return found

        found = 0
        for cave in self._connections[visited.last]:
            if cave == "start":
                # Cannot return to starting cave.
                continue
            elif cave == "end":
                # Reached the final cave.
                found += 1
                continue

            next_visited = visited.append(cave)
            if next_visited is None:
                # Path with next cave is not valid.
                continue

            found += self._count_paths(next_visited, cache)

        cache[visited] = found
        return found


def _parse_connection(s: str) -> Tuple[str, str]:
    start, end = s.strip().split("-")
    return start, end


def _create_cavern() -> Cavern:
    with open_text("aoc21.days", "day12.txt") as f:
        return Cavern(map(_parse_connection, f))


def _path_has_small_cave(path: Sequence[str]) -> bool:
    assert path[0] == "start" and path[-1] == "end"
    return any(path[i].islower() for i in range(1, len(path) - 1))


def part1() -> object:
    return _create_cavern().count_paths(visit_once=True)


def part2() -> object:
    return _create_cavern().count_paths(visit_once=False)
