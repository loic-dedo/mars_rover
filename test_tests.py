import pytest

from rover import Map, Rover

map_25 = Map(25, 25)
map_10 = Map(
    10,
    10,
    [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    ],
)


@pytest.mark.parametrize(
    "x,y,direction",
    [
        (0, 0, "N"),
        (5, 5, "E"),
        (10, 10, "S"),
        (15, 15, "W"),
    ],
)
def test_rover_initialization(x, y, direction):
    rover = Rover((x, y), direction, map_25)
    assert rover.x == x
    assert rover.y == y
    assert rover.direction == direction


@pytest.mark.parametrize(
    "x,y,direction,expected_x,expected_y",
    [
        (0, 1, "N", 0, 0),
        (5, 5, "E", 6, 5),
        (10, 10, "S", 10, 11),
        (15, 15, "W", 14, 15),
    ],
)
def test_rover_move_forward(x, y, direction, expected_x, expected_y):
    rover = Rover((x, y), direction, map_25)
    rover.move_forward()
    assert rover.x == expected_x
    assert rover.y == expected_y
    assert rover.direction == direction


@pytest.mark.parametrize(
    "x,y,direction,expected_x,expected_y",
    [
        (0, 0, "N", 0, 1),
        (5, 5, "E", 4, 5),
        (10, 10, "S", 10, 9),
        (15, 15, "W", 16, 15),
    ],
)
def test_rover_move_backward(x, y, direction, expected_x, expected_y):
    rover = Rover((x, y), direction, map_25)
    rover.move_backward()
    assert rover.x == expected_x
    assert rover.y == expected_y
    assert rover.direction == direction


@pytest.mark.parametrize(
    "direction,expected_direction",
    [
        ("N", "W"),
        ("W", "S"),
        ("S", "E"),
        ("E", "N"),
    ],
)
def test_rover_turn_left(direction, expected_direction):
    rover = Rover((0, 0), direction, map_25)
    rover.turn_left()
    assert rover.direction == expected_direction


@pytest.mark.parametrize(
    "direction,expected_direction",
    [
        ("N", "E"),
        ("E", "S"),
        ("S", "W"),
        ("W", "N"),
    ],
)
def test_rover_turn_right(direction, expected_direction):
    rover = Rover((0, 0), direction, map_25)
    rover.turn_right()
    assert rover.direction == expected_direction


@pytest.mark.parametrize(
    "x,y,direction,commands,expected_x,expected_y,expected_direction",
    [
        (0, 3, "N", "fbffb", 0, 2, "N"),
        (5, 5, "E", "fff", 8, 5, "E"),
        (10, 10, "S", "bbb", 10, 7, "S"),
        (15, 15, "W", "bbfbbfb", 18, 15, "W"),
        (2, 1, "N", "fblffb", 1, 1, "W"),
        (5, 5, "E", "frfrf", 5, 6, "W"),
        (10, 10, "S", "BLbrB", 9, 8, "S"),
        (15, 15, "W", "RBBFBBFB", 15, 18, "N"),
    ],
)
def test_rover_execute_commands(
    x, y, direction, commands, expected_x, expected_y, expected_direction
):
    rover = Rover((x, y), direction, map_25)
    rover.execute_commands(commands)
    assert rover.x == expected_x
    assert rover.y == expected_y
    assert rover.direction == expected_direction


@pytest.mark.parametrize(
    "x,y,direction,commands,expected_x,expected_y,expected_direction",
    [
        (2, 0, "N", "F", 2, 9, "N"),
        (9, 2, "E", "F", 0, 2, "E"),
        (2, 9, "S", "F", 2, 0, "S"),
        (0, 2, "W", "F", 9, 2, "W"),
    ],
)
def test_edges_wrapping(
    x, y, direction, commands, expected_x, expected_y, expected_direction
):
    rover = Rover((x, y), direction, map_10)
    rover.execute_commands(commands)
    assert rover.x == expected_x
    assert rover.y == expected_y
    assert rover.direction == expected_direction


@pytest.mark.parametrize(
    "x,y,direction,expected_x,expected_y",
    [
        (0, 0, "N", 0, 6),
        (0, 1, "N", 0, 1),
        (9, 8, "S", 9, 8),
    ],
)
def test_obstacles_detection(x, y, direction, expected_x, expected_y):
    rover = Rover((x, y), direction, map_10)
    rover.execute_commands("FFFF")
    assert rover.x == expected_x
    assert rover.y == expected_y
    assert rover.direction == direction
