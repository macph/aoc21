from aoc21.days.day05 import Position, Line


def test_parse_position():
    assert Position.parse("-1, 9") == Position(-1, 9)


def test_parse_line():
    assert Line.parse("-1, 5 -> 3, 5") == Line(Position(-1, 5), Position(3, 5))


def test_positions():
    line = Line(Position(0, 5), Position(4, 5))
    assert list(line.positions()) == [
        Position(0, 5),
        Position(1, 5),
        Position(2, 5),
        Position(3, 5),
        Position(4, 5),
    ]


def test_positions_reverse():
    line = Line(Position(1, 5), Position(1, 1))
    assert list(line.positions()) == [
        Position(1, 5),
        Position(1, 4),
        Position(1, 3),
        Position(1, 2),
        Position(1, 1),
    ]
