"""
Advent of Code 2018, Day 1
Chronal Calibration
https://adventofcode.com/2018/day/1
"""

from itertools import cycle
from os import path

INPUT_FILE = "input.txt"


def read_frequencies(file_path: str) -> list[int]:
    """Read frequencies from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [int(line) for line in file]


def get_final_frequency(frequencies: list[int]) -> int:
    """Calculate the final frequency."""

    return sum(frequencies)


def find_first_repeat_frequency(frequencies: list[int]) -> int:
    """Find the first frequency that appears twice."""

    seen_frequencies = {0}
    current_frequency = 0

    for frequency_change in cycle(frequencies):
        current_frequency += frequency_change

        if current_frequency in seen_frequencies:
            return current_frequency

        seen_frequencies.add(current_frequency)

    raise ValueError("No frequency repeated.")


def main() -> None:
    """Read frequencies from a file and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    frequencies = read_frequencies(file_path)
    print(frequencies)

    final_frequency = get_final_frequency(frequencies)
    print(f"The final frequency is {final_frequency}.")

    first_repeat_frequency = find_first_repeat_frequency(frequencies)
    print(f"The first frequency that appears twice is {first_repeat_frequency}.")


if __name__ == "__main__":
    main()
