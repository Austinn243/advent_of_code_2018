"""
Advent of Code 2018, Day 2
Inventory Management System
https://adventofcode.com/2018/day/2
"""

from collections import Counter
from itertools import pairwise
from os import path

INPUT_FILE = "input.txt"
TEST_FILE_1 = "test1.txt"
TEST_FILE_2 = "test2.txt"


def read_box_ids(file_path: str) -> list[str]:
    """Read box ids from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [line.strip() for line in file]


def checksum(box_ids: str) -> int:
    """Calculate the checksum of a collection of box ids."""

    two_frequency_count = 0
    three_frequency_count = 0

    for box_id in box_ids:
        char_counts = Counter(box_id)

        has_two_frequency = any(count == 2 for count in char_counts.values())
        if has_two_frequency > 0:
            two_frequency_count += 1

        has_three_frequency = any(count == 3 for count in char_counts.values())
        if has_three_frequency > 0:
            three_frequency_count += 1

    return two_frequency_count * three_frequency_count


def find_correct_box_ids(box_ids: list[str]) -> list[str]:
    """Find the two correct box IDs."""

    sorted_box_ids = sorted(box_ids)

    try:
        correct_box_ids = next(
            (box_id1, box_id2)
            for box_id1, box_id2 in pairwise(sorted_box_ids)
            if are_correct_box_ids(box_id1, box_id2)
        )
        return correct_box_ids
    except StopIteration as e:
        raise ValueError("No correct box IDs found.") from e


def are_correct_box_ids(box_id1: str, box_id2: str) -> bool:
    """Check if the two box IDs are the ones we are looking for.

    The box IDs are correct if they differ by exactly one character
    at the same position in both ids.
    """

    seen_difference = False

    for char1, char2 in zip(box_id1, box_id2):
        if char1 == char2:
            continue

        if seen_difference:
            return False

        seen_difference = True

    return seen_difference


def get_common_letters(box_id1: str, box_id2: str) -> list[str]:
    """Get the common letters between two box IDs."""

    return [letter1 for letter1, letter2 in zip(box_id1, box_id2) if letter1 == letter2]


def main() -> None:
    """Read box IDs from a file and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    box_ids = read_box_ids(file_path)
    print(box_ids)

    box_ids_checksum = checksum(box_ids)
    print(f"The checksum is {box_ids_checksum}")

    correct_box_ids = find_correct_box_ids(box_ids)
    print(correct_box_ids)

    common_letters = get_common_letters(*correct_box_ids)
    print(f"The common letters are {''.join(common_letters)}.")


if __name__ == "__main__":
    main()
