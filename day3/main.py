"""
Advent of Code 2018, Day 3
No Matter How You Slice It
https://adventofcode.com/2018/day/3
"""

import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from os import path
from typing import NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

CLAIM_REGEX = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
FABRIC_SIDE_LENGTH = 1000


@dataclass(frozen=True)
class Claim:
    """Represents a claim for a piece of fabric."""

    id: int
    x: int
    y: int
    width: int
    height: int

    def __repr__(self) -> str:
        """Return a string representation of the claim for debugging purposes."""

        return (
            "Claim("
            f"id={self.id}, "
            f"x={self.x}, "
            f"y={self.y}, "
            f"width={self.width}, "
            f"height={self.height})"
        )


class Position(NamedTuple):
    """Represents a position on a 2D grid."""

    x: int
    y: int


def read_claims(file_path: str) -> list[Claim]:
    """Read claims from a file."""

    with open(file_path) as file:
        return [parse_claim(line) for line in file]


def parse_claim(line: str) -> Claim:
    """Parse a claim from a line of text."""

    match = CLAIM_REGEX.match(line)
    if not match:
        raise ValueError(f"Invalid claim: {line}")

    claim_id, x, y, width, height = [int(value) for value in match.groups()]

    return Claim(claim_id, x, y, width, height)


def count_position_overlap(claims: list[Claim]) -> dict[Position, int]:
    """Count the number of claims that overlap at each position."""

    position_overlap_counts: dict[Position, int] = defaultdict(int)

    for claim in claims:
        x_range = range(claim.x, claim.x + claim.width)
        y_range = range(claim.y, claim.y + claim.height)

        for x, y in product(x_range, y_range):
            position_overlap_counts[Position(x, y)] += 1

    return position_overlap_counts


def count_overlapping_square_inches(claims: list[Claim]) -> int:
    """Count the number of square inches that are claimed by multiple claims."""

    position_overlap_counts = count_position_overlap(claims)

    return sum(count > 1 for count in position_overlap_counts.values())


def find_non_overlapping_claim(claims: list[Claim]) -> Claim:
    """Find the claim that does not overlap with any other claim."""

    position_overlap_counts = count_position_overlap(claims)

    for claim in claims:
        x_range = range(claim.x, claim.x + claim.width)
        y_range = range(claim.y, claim.y + claim.height)

        if all(
            position_overlap_counts[Position(x, y)] == 1
            for x, y in product(x_range, y_range)
        ):
            return claim

    raise ValueError("No non-overlapping claim found")


def main() -> None:
    """Read claims from an input file and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    claims = read_claims(file_path)
    print(claims)

    overlapping_square_inches = count_overlapping_square_inches(claims)
    print(f"Overlapping square inches: {overlapping_square_inches}")

    non_overlapping_claim = find_non_overlapping_claim(claims)
    print(f"Non-overlapping claim: {non_overlapping_claim}")


if __name__ == "__main__":
    main()
