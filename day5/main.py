"""
Advent of Code 2018, Day 5
Alchemical Reduction
https://adventofcode.com/2018/day/5
"""

from os import path

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def read_polymer(file_path: str) -> str:
    """Read a polymer from a file."""

    with open(file_path) as file:
        return file.read().strip()


def should_react(unit1: str, unit2: str) -> bool:
    """Determine whether two units should react."""

    same_type = unit1.lower() == unit2.lower()
    opposite_polarity = unit1.islower() != unit2.islower()

    return same_type and opposite_polarity


def reduce_polymer(polymer: str) -> str:
    """Reduce a polymer to its simplest form.

    Adjacent units of the same type and opposite polarity will react and be destroyed.
    """

    remaining_units = [polymer[0]]

    for unit in polymer[1:]:
        if remaining_units and should_react(unit, remaining_units[-1]):
            remaining_units.pop()
        else:
            remaining_units.append(unit)

    return "".join(remaining_units)


def remove_unit(polymer: str, unit: str) -> str:
    """Remove all units of a given type from a polymer."""

    return polymer.replace(unit.lower(), "").replace(unit.upper(), "")


def find_smallest_polymer_after_unit_removal(polymer: str) -> str:
    """Find the smallest polymer that results from removing one unit type."""

    units = set(polymer.lower())

    polymer_variants = [remove_unit(polymer, unit) for unit in units]

    reduced_polymer_variants = [reduce_polymer(variant) for variant in polymer_variants]

    return min(reduced_polymer_variants, key=len)


def main() -> None:
    """Read the polymer from a file and process it."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    polymer = read_polymer(file_path)
    print(polymer)

    reduced_polymer = reduce_polymer(polymer)
    print(reduced_polymer)
    print(len(reduced_polymer))

    smallest_possible_polymer = find_smallest_polymer_after_unit_removal(polymer)
    print(smallest_possible_polymer)
    print(len(smallest_possible_polymer))


if __name__ == "__main__":
    main()
