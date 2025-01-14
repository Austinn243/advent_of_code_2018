"""
Advent of Code 2018, Day 4
Repose Record
https://adventofcode.com/2018/day/4
"""

import re
from dataclasses import dataclass
from datetime import datetime
from os import path
from pprint import pprint
from typing import NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


TIMESTAMP_PATTERN = r"\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\]"
SHIFT_START_PATTERN = r"Guard #(\d+) begins shift"
SLEEP_PATTERN = r"falls asleep"
WAKE_PATTERN = r"wakes up"

SHIFT_START_REGEX = re.compile(TIMESTAMP_PATTERN + " " + SHIFT_START_PATTERN)
SLEEP_REGEX = re.compile(TIMESTAMP_PATTERN + " " + SLEEP_PATTERN)
WAKE_REGEX = re.compile(TIMESTAMP_PATTERN + " " + WAKE_PATTERN)

RECORD_REGEXES = [SHIFT_START_REGEX, SLEEP_REGEX, WAKE_REGEX]


class ShiftStartRecord(NamedTuple):
    """Represents a record of a guard starting a shift."""

    timestamp: datetime
    guard_id: int


class SleepRecord(NamedTuple):
    """Represents a record of a guard falling asleep."""

    timestamp: datetime


class WakeRecord(NamedTuple):
    """Represents a record of a guard waking up."""

    timestamp: datetime


Record = ShiftStartRecord | SleepRecord | WakeRecord


@dataclass(frozen=True)
class GuardActivityLog:
    """Represents a consolidated log of a guard's activity throughout the year."""

    guard_id: int


def read_records(file_path: str) -> list[Record]:
    """Read records of guard activity from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [parse_record(line) for line in file]


def parse_record(line: str) -> Record:
    """Parse a record from a line of text."""

    pattern_regex = None
    matches = None
    for regex in RECORD_REGEXES:
        matches = regex.match(line)
        if matches:
            matches = matches
            pattern_regex = regex
            break

    if not matches:
        raise ValueError(f"Invalid record: {line}")

    year, month, day, hour, minute = map(int, matches.groups()[:5])
    timestamp = datetime(year, month, day, hour, minute)

    if pattern_regex is SHIFT_START_REGEX:
        guard_id = int(matches.group(6))
        return ShiftStartRecord(timestamp, guard_id)

    if pattern_regex is SLEEP_REGEX:
        return SleepRecord(timestamp)

    return WakeRecord(timestamp)


def consolidate_records(records: list[Record]) -> dict[int, GuardActivityLog]:
    """Consolidate records of guard activity into a log of each guard's activity."""

    guard_activity_logs: dict[int, GuardActivityLog] = {}

    active_guard_id = None
    previous_timestamp = None

    return guard_activity_logs


def main() -> None:
    """Read records of guard activity from a file and process them."""

    input_file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), input_file)

    records = read_records(file_path)
    sorted_records = sorted(records, key=lambda record: record.timestamp)
    pprint(sorted_records)


if __name__ == "__main__":
    main()
