from aoc21.days.day09 import HeightMap, Point


def test_position_add():
    assert Point(10, 20) + Point(5, -5) == Point(15, 15)


HEIGHT_MAP = HeightMap(
    [
        [2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
        [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
        [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
        [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
        [9, 8, 9, 9, 9, 6, 5, 6, 7, 8],
    ]
)


def test_parse_height_map():
    map_input = "2199943210\n3987894921\n9856789892\n8767896789\n9899965678\n"
    height_map = HeightMap.parse(map_input)
    assert list(height_map.values()) == list(HEIGHT_MAP.values())


def test_height_map_get_item():
    assert HEIGHT_MAP[Point(0, 0)] == 2
    assert HEIGHT_MAP[Point(0, 1)] == 3
    assert HEIGHT_MAP[Point(1, 0)] == 1
    assert HEIGHT_MAP[Point(1, 1)] == 9


def test_height_map_iter():
    assert list(HEIGHT_MAP) == [Point(i, j) for j in range(5) for i in range(10)]


def test_height_map_get_adjacent():
    assert list(HEIGHT_MAP.get_adjacent_points(Point(2, 2))) == [
        Point(1, 2),
        Point(3, 2),
        Point(2, 1),
        Point(2, 3),
    ]


def test_height_map_get_adjacent_top_left():
    assert list(HEIGHT_MAP.get_adjacent_points(Point(0, 0))) == [
        Point(1, 0),
        Point(0, 1),
    ]


def test_height_map_get_adjacent_bottom_right():
    assert list(HEIGHT_MAP.get_adjacent_points(Point(9, 4))) == [
        Point(8, 4),
        Point(9, 3),
    ]


def test_height_map_low_points():
    assert list(HEIGHT_MAP.find_low_points()) == [
        Point(1, 0),
        Point(9, 0),
        Point(2, 2),
        Point(6, 4),
    ]


def test_height_map_risk_levels():
    assert list(map(HEIGHT_MAP.get_risk_level, HEIGHT_MAP.find_low_points())) == [
        2,
        1,
        6,
        6,
    ]


def test_height_map_basins():
    assert list(HEIGHT_MAP.find_basins()) == [
        {Point(0, 0), Point(1, 0), Point(0, 1)},
        {
            Point(5, 0),
            Point(6, 0),
            Point(7, 0),
            Point(8, 0),
            Point(9, 0),
            Point(6, 1),
            Point(8, 1),
            Point(9, 1),
            Point(9, 2),
        },
        {
            Point(2, 1),
            Point(3, 1),
            Point(4, 1),
            Point(1, 2),
            Point(2, 2),
            Point(3, 2),
            Point(4, 2),
            Point(5, 2),
            Point(0, 3),
            Point(1, 3),
            Point(2, 3),
            Point(3, 3),
            Point(4, 3),
            Point(1, 4),
        },
        {
            Point(7, 2),
            Point(6, 3),
            Point(7, 3),
            Point(8, 3),
            Point(5, 4),
            Point(6, 4),
            Point(7, 4),
            Point(8, 4),
            Point(9, 4),
        },
    ]
