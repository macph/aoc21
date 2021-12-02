from enum import Enum
from importlib.resources import open_text
from typing import Iterable, List, NamedTuple, Tuple


class CommandType(Enum):
    FORWARD = "forward"
    DOWN = "down"
    UP = "up"


class Command(NamedTuple):
    type: CommandType
    value: int

    @classmethod
    def parse(cls, string: str) -> "Command":
        try:
            command, value = string.split()
            return cls(CommandType(command), int(value))
        except ValueError as e:
            raise ValueError(
                "Expected command in form '[forward|down|up] [integer]'."
            ) from e


def _get_commands() -> List[Command]:
    with open_text("aoc21.days", "day02.txt") as f:
        return list(map(Command.parse, f))


def apply_commands(commands: Iterable[Command]) -> Tuple[int, int]:
    horizontal, vertical = 0, 0
    for c in commands:
        if c.type == CommandType.FORWARD:
            horizontal += c.value
        elif c.type == CommandType.DOWN:
            vertical += c.value
        elif c.type == CommandType.UP:
            vertical -= c.value
        else:
            raise ValueError(f"Unexpected command: {c!r}.")

    return horizontal, vertical


def apply_commands_with_aim(commands: Iterable[Command]) -> Tuple[int, int]:
    horizontal, vertical, aim = 0, 0, 0
    for c in commands:
        if c.type == CommandType.FORWARD:
            horizontal += c.value
            vertical += aim * c.value
        elif c.type == CommandType.DOWN:
            aim += c.value
        elif c.type == CommandType.UP:
            aim -= c.value
        else:
            raise ValueError(f"Unexpected command: {c!r}.")

    return horizontal, vertical


def part1() -> object:
    horizontal, vertical = apply_commands(_get_commands())

    return horizontal * vertical


def part2() -> object:
    horizontal, vertical = apply_commands_with_aim(_get_commands())

    return horizontal * vertical
