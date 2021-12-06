from aoc21.days.day06 import School


def test_school_step():
    school = School([3, 4, 3, 1, 2])

    school.step()
    assert school.size == 5

    school.step()
    assert school.size == 6

    school.step()
    assert school.size == 7

    school.step()
    assert school.size == 9

    school.step()
    assert school.size == 10
