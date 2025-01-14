"""
Advent of Code 2018, Day 8
Memory Maneuver
https://adventofcode.com/2018/day/8
"""

from dataclasses import dataclass
from os import path

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


HEADER_DATA_SIZE = 2


@dataclass(frozen=True)
class LicenseTree:
    """A node in a license tree."""

    children: list["LicenseTree"]
    metadata: list[int]

    def __len__(self) -> int:
        """Retrieve the size of the node."""

        child_sizes = [len(child) for child in self.children]
        return HEADER_DATA_SIZE + sum(child_sizes) + len(self.metadata)

    @property
    def value(self) -> int:
        """Retrieve the value of the node."""

        if not self.children:
            return sum(self.metadata)

        value = 0

        for child_number in self.metadata:
            has_nth_child = 1 <= child_number <= len(self.children)
            value += self.children[child_number - 1].value if has_nth_child else 0

        return value


def read_license(file_path: str) -> list[int]:
    """Read a license from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [int(num) for num in file.read().strip().split()]


def create_license_tree(license_data: list[int]) -> LicenseTree:
    """Create a tree structure from license data."""

    return create_node(license_data, 0)


def create_node(license_data: list[int], start: int) -> LicenseTree:
    """Create a node from license data."""

    pointer = start

    child_count = license_data[pointer]
    metadata_entry_count = license_data[pointer + 1]

    pointer += HEADER_DATA_SIZE

    children = []
    for _ in range(child_count):
        child = create_node(license_data, pointer)
        pointer += len(child)
        children.append(child)

    metadata = license_data[pointer : pointer + metadata_entry_count]
    return LicenseTree(children, metadata)


def sum_metadata(license_tree: LicenseTree) -> int:
    """Sum the metadata entries in a license."""

    child_sums = [sum_metadata(child) for child in license_tree.children]

    return sum(license_tree.metadata) + sum(child_sums)


def main() -> None:
    """Read a license from a file and process it."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    license_data = read_license(file_path)
    license_tree = create_license_tree(license_data)

    print(f"The sum of all nodes' metadata is {sum_metadata(license_tree)}")
    print(f"The value of the root node is {license_tree.value}")


if __name__ == "__main__":
    main()
