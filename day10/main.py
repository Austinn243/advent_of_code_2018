"""
Advent of Code 2018, Day 10
The Stars Align
https://adventofcode.com/2018/day/10
"""

import re
from os import path
from typing import NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


VECTOR_PATTERN = r"<\s?(-?\d+),\s+(-?\d+)>"
POINT_REGEX = re.compile(r"position=" + VECTOR_PATTERN + r" velocity=" + VECTOR_PATTERN)


class Vector(NamedTuple):
    """A vector in two-dimensional space."""

    x: int
    y: int


class Point(NamedTuple):
    """A point of light in two-dimensional space."""

    position: Vector
    velocity: Vector


class BoundingBox(NamedTuple):
    """A bounding box in two-dimensional space."""

    width: int
    height: int


Grid = list[list[str]]


def read_point_data(file_path: str) -> list[Point]:
    """Read point data from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [parse_point(line) for line in file]


def parse_point(line: str) -> Point:
    """Parse a point of light from a line."""

    match = POINT_REGEX.match(line)
    if not match:
        raise ValueError(f"Invalid point data: {line}")

    position = Vector(int(match.group(1)), int(match.group(2)))
    velocity = Vector(int(match.group(3)), int(match.group(4)))

    return Point(position, velocity)


def advance_point(point: Point, seconds: int = 1) -> Point:
    """Determine the position of a point after a number of seconds."""

    position, velocity = point

    x_displacement = velocity.x * seconds
    y_displacement = velocity.y * seconds

    new_position = Vector(position.x + x_displacement, position.y + y_displacement)

    return Point(new_position, velocity)


def get_bounding_box(points: list[Point]) -> BoundingBox:
    """Determine the bounding box that contains all points of light."""

    min_x = min(point.position.x for point in points)
    max_x = max(point.position.x for point in points)
    min_y = min(point.position.y for point in points)
    max_y = max(point.position.y for point in points)

    width = max_x - min_x
    height = max_y - min_y

    return BoundingBox(width, height)


def get_grid_and_time_for_message(points: list[Point]) -> tuple[Grid, int]:
    """Determine the grid and time at which the message appears."""

    current_points = points
    current_bounding_box = get_bounding_box(points)
    elapsed_time = 0

    while True:
        next_points = [advance_point(point, elapsed_time + 1) for point in points]
        next_bounding_box = get_bounding_box(next_points)
        if next_bounding_box.width > current_bounding_box.width:
            break

        current_bounding_box = next_bounding_box
        current_points = next_points
        elapsed_time += 1

    return create_points_grid(current_points), elapsed_time


def create_points_grid(points: list[Point]) -> Grid:
    """Create a grid with points of light."""

    min_x = min(point.position.x for point in points)
    max_x = max(point.position.x for point in points)
    min_y = min(point.position.y for point in points)
    max_y = max(point.position.y for point in points)

    grid = [["."] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]

    for point in points:
        x = point.position.x - min_x
        y = point.position.y - min_y
        grid[y][x] = "#"

    return grid


def print_grid(grid: Grid) -> None:
    """Print a grid."""

    for row in grid:
        print("".join(row))


def main() -> None:
    """Read information about moving points of light and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    points = read_point_data(file_path)

    message_grid, message_time = get_grid_and_time_for_message(points)
    print("The message that will appear in the sky is:")
    print_grid(message_grid)
    print(f"The message will appear after {message_time} seconds.")


if __name__ == "__main__":
    main()
