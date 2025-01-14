"""
Advent of Code 2018, Day 11
Chronal Charge
https://adventofcode.com/2018/day/11
"""

from itertools import product
from typing import NamedTuple

INPUT_SERIAL_NUMBER = 9110
TEST_SERIAL_NUMBER_1 = 8
TEST_SERIAL_NUMBER_2 = 18
TEST_SERIAL_NUMBER_3 = 42

GRID_HEIGHT = 300
GRID_WIDTH = 300


class Position(NamedTuple):
    """Represents a position on the grid."""

    x: int
    y: int


class SubgridIdentifier(NamedTuple):
    """Identifies a subgrid on the grid."""

    top_left_coordinate: Position
    side_length: int


PowerGrid = list[list[int]]


def get_power_level(fuel_cell_position: Position, serial_number: int) -> int:
    """Get the power level of a cell."""

    x, y = fuel_cell_position

    rack_id = x + 10

    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id

    hundreds_digit = power_level // 100 % 10
    power_level = hundreds_digit
    power_level -= 5

    return power_level


def create_power_grid(serial_number: int) -> PowerGrid:
    """Create a 300x300 power grid."""

    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    x_range = range(GRID_WIDTH)
    y_range = range(GRID_HEIGHT)

    for x, y in product(x_range, y_range):
        grid[y][x] = get_power_level(Position(x, y), serial_number)

    return grid


def get_total_power_of_subgrid(
    grid: PowerGrid,
    subgrid_identifier: SubgridIdentifier,
) -> int:
    """Get the total power of a subgrid."""

    (x, y), side_length = subgrid_identifier

    x_offset_range = range(side_length)
    y_offset_range = range(side_length)

    power_levels = []

    for dx, dy in product(x_offset_range, y_offset_range):
        power_levels.append(grid[y + dy][x + dx])

    return sum(power_levels)


def find_largest_power_3_by_3_subgrid(grid: PowerGrid) -> SubgridIdentifier:
    """Find the 3 by 3 subgrid with the largest total power."""

    x_range = range(0, GRID_WIDTH - 2)
    y_range = range(0, GRID_HEIGHT - 2)

    max_power_level = float("-inf")
    largest_subgrid_identifier = SubgridIdentifier(Position(0, 0), 1)

    for x, y in product(x_range, y_range):
        subgrid_identifier = SubgridIdentifier(Position(x, y), 3)

        subgrid_power_level = get_total_power_of_subgrid(grid, subgrid_identifier)
        if subgrid_power_level <= max_power_level:
            continue

        max_power_level = subgrid_power_level
        largest_subgrid_identifier = subgrid_identifier

    return largest_subgrid_identifier


def main() -> None:
    """Process data about the power grid using the given serial number."""

    serial_number = TEST_SERIAL_NUMBER_2

    power_grid = create_power_grid(serial_number)

    largest_3_by_3_subgrid = find_largest_power_3_by_3_subgrid(power_grid)
    print(largest_3_by_3_subgrid)


if __name__ == "__main__":
    main()
