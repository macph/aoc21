from aoc21.days.day04 import Board, BoardScore

NUMBERS = [
    7,
    4,
    9,
    5,
    11,
    17,
    23,
    2,
    0,
    14,
    21,
    24,
    10,
    16,
    13,
    6,
    25,
    12,
    22,
    18,
    20,
    8,
    19,
    3,
    26,
    1,
]

BOARD = Board(
    [
        22,
        13,
        17,
        11,
        0,
        8,
        2,
        23,
        4,
        24,
        21,
        9,
        14,
        16,
        7,
        6,
        10,
        3,
        18,
        5,
        1,
        12,
        20,
        15,
        19,
    ]
)


def test_board_row():
    assert list(BOARD.row(0)) == [22, 13, 17, 11, 0]
    assert list(BOARD.row(2)) == [21, 9, 14, 16, 7]
    assert list(BOARD.row(4)) == [1, 12, 20, 15, 19]


def test_board_column():
    assert list(BOARD.column(0)) == [22, 8, 21, 6, 1]
    assert list(BOARD.column(2)) == [17, 23, 14, 3, 20]
    assert list(BOARD.column(4)) == [0, 24, 7, 5, 19]


def test_board_draw_until_complete():
    final_number = 16
    sum_remaining = 137
    number_index = 13
    assert BOARD.draw_until_complete(NUMBERS) == BoardScore(
        number_index, final_number * sum_remaining
    )
