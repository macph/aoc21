import pytest

from aoc21.days.day02 import (
    apply_commands,
    apply_commands_with_aim,
    Command,
    CommandType,
)


@pytest.mark.parametrize(
    "string, expected",
    [
        ("forward 5", Command(CommandType.FORWARD, 5)),
        ("down 5", Command(CommandType.DOWN, 5)),
        ("up 3", Command(CommandType.UP, 3)),
    ],
)
def test_parse_command(string, expected):
    assert Command.parse(string) == expected


COMMANDS = [
    Command(CommandType.FORWARD, 5),
    Command(CommandType.DOWN, 5),
    Command(CommandType.FORWARD, 8),
    Command(CommandType.UP, 3),
    Command(CommandType.DOWN, 8),
    Command(CommandType.FORWARD, 2),
]


def test_apply_commands():
    assert apply_commands(COMMANDS) == (15, 10)


def test_apply_commands_with_aim():
    assert apply_commands_with_aim(COMMANDS) == (15, 60)
