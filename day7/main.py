"""
Advent of Code 2018, Day 7
The Sum of Its Parts
https://adventofcode.com/2018/day/7
"""

import re
from heapq import heappop, heappush
from os import path
from pprint import pprint
from typing import NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

INSTRUCTION_REGEX = re.compile(
    r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.",
)

BASE_STEP_COMPLETION_TIME = 60
DEFAULT_WORKER_COUNT = 5


class Instruction(NamedTuple):
    """Represents an instruction for a step in a sequence."""

    step: str
    dependency: str


def read_instructions(file_path: str) -> list[Instruction]:
    """Read instructions from a file."""

    with open(file_path) as file:
        return [parse_instruction(line.strip()) for line in file]


def parse_instruction(line: str) -> Instruction:
    """Parse an instruction from a line of text."""

    regex_match = INSTRUCTION_REGEX.match(line)
    if not regex_match:
        raise ValueError(f"Invalid instruction: {line}")

    dependency = regex_match.group(1)
    step = regex_match.group(2)

    return Instruction(step, dependency)


def create_dependency_graph(instructions: list[Instruction]) -> dict[str, set[str]]:
    """Create a graph of step dependencies."""

    graph: dict[str, set[str]] = {}

    for step, dependency in instructions:
        if step not in graph:
            graph[step] = set()

        if dependency not in graph:
            graph[dependency] = set()

        graph[step].add(dependency)

    return graph


def find_initial_steps(graph: dict[str, set[str]]) -> list[str]:
    """Find the steps that have no dependencies."""

    return [step for step, dependencies in graph.items() if not dependencies]


def create_step_queue(graph: dict[str, set[str]]) -> list[str]:
    """Prepare a queue of steps to be completed."""

    next_steps = []

    for step in find_initial_steps(graph):
        heappush(next_steps, step)

    return next_steps


def find_completion_order(instructions: list[Instruction]) -> list[str]:
    """Find the order in which steps should be completed.

    Steps should be completed first if they have no dependencies then in
    alphabetical order.
    """

    graph = create_dependency_graph(instructions)

    completion_order = []
    next_steps = create_step_queue(graph)

    # NOTE: By using a priority queue over a standard queue for organizing the
    # next steps, we automatically sort the steps in alphabetical order when
    # enqueueing them as characters are compared by their character codes.

    while next_steps:
        current_step = heappop(next_steps)

        completion_order.append(current_step)

        for step, dependencies in graph.items():
            if current_step not in dependencies:
                continue

            dependencies.remove(current_step)

            if not dependencies:
                heappush(next_steps, step)

    return completion_order


def get_step_completion_time(
    step: str,
    base_completion_time: int = BASE_STEP_COMPLETION_TIME,
) -> int:
    """Determine the number of seconds it takes to complete a step."""

    step_specific_time = ord(step) - ord("A") + 1

    return base_completion_time + step_specific_time


def get_total_completion_time(
    instructions: list[Instruction],
    base_step_completion_time: int = BASE_STEP_COMPLETION_TIME,
    worker_count: int = DEFAULT_WORKER_COUNT,
) -> int:
    """Determine how long it will take to complete all steps."""

    def create_new_tasks(
        available_steps: list[str],
        available_worker_count: int,
    ) -> list[tuple[str, int]]:
        """Create new tasks for available workers."""

        new_worker_tasks = []

        while available_worker_count > 0 and available_steps:
            next_step = heappop(available_steps)
            new_task = (
                next_step,
                get_step_completion_time(next_step, base_step_completion_time),
            )

            new_worker_tasks.append(new_task)

        return new_worker_tasks

    graph = create_dependency_graph(instructions)

    worker_tasks = []
    available_worker_count = worker_count

    available_steps = create_step_queue(graph)

    remaining_step_count = len(graph)
    elapsed_time = 0

    while remaining_step_count > 0:
        new_tasks = create_new_tasks(available_steps, available_worker_count)
        available_worker_count -= len(new_tasks)
        worker_tasks.extend(new_tasks)

        updated_tasks = []
        for assigned_step, current_time in worker_tasks:
            updated_time = current_time - 1

            if updated_time > 0:
                updated_tasks.append((assigned_step, updated_time))
                continue

            available_worker_count += 1
            remaining_step_count -= 1

            for step, dependencies in graph.items():
                if assigned_step not in dependencies:
                    continue

                dependencies.remove(assigned_step)

                if not dependencies:
                    heappush(available_steps, step)

        elapsed_time += 1
        worker_tasks = updated_tasks

    return elapsed_time


def main() -> None:
    """Read instructions from a file and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    instructions = read_instructions(file_path)
    pprint(instructions)

    completion_order = find_completion_order(instructions)
    print(f"The correct completion order is {"".join(completion_order)}")

    total_completion_time = get_total_completion_time(instructions)
    print(f"The total completion time is {total_completion_time}")


if __name__ == "__main__":
    main()


# 250 is too low.
# 899 is too high.
# 959 is too high.
