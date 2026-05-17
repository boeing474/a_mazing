"""Configuration parsing and validation for the A-Maze-ing application."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .model import Coordinate


REQUIRED_KEYS = frozenset({
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
})


class MazeConfigError(Exception):
    """Raised when the configuration file contains invalid syntax or values."""


@dataclass(frozen=True)
class MazeConfig:
    """Immutable, validated configuration parameters required to build a maze.
    """

    width: int
    height: int
    entry: Coordinate
    exit: Coordinate
    output_file: Path
    perfect: bool
    seed: int | str | None = None


def load_config(path_str: str) -> MazeConfig:
    """Read, parse, and validate a maze configuration file from the filesystem.
    """

    config_path = Path(path_str)
    if not config_path.is_file():
        raise MazeConfigError(f"Configuration file not found: {config_path}")

    try:
        lines = config_path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise MazeConfigError(f"Failed to read configuration file: "
                              f"{config_path}") from error

    raw_values: dict[str, str] = {}
    for line_num, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split("=", maxsplit=1)
        if len(parts) != 2:
            raise MazeConfigError(
                f"Syntax error on line {line_num}: Expected 'KEY=VALUE' format"
                f"."
            )

        key, value = parts[0].strip(), parts[1].strip()
        if not key or not value:
            raise MazeConfigError(
                f"Syntax error on line {line_num}: Key or value cannot be "
                f"empty."
            )

        if key in raw_values:
            raise MazeConfigError(f"Duplicate configuration key on line "
                                  f"{line_num}: '{key}'")

        raw_values[key] = value

    # Check for missing mandatory keys using set difference
    missing_keys = REQUIRED_KEYS - raw_values.keys()
    if missing_keys:
        missing_str = ", ".join(sorted(missing_keys))
        raise MazeConfigError(f"Missing mandatory configuration keys: "
                              f"{missing_str}")

    width = _parse_positive_int(raw_values["WIDTH"], "WIDTH")
    height = _parse_positive_int(raw_values["HEIGHT"], "HEIGHT")
    entry = _parse_coordinate(raw_values["ENTRY"], "ENTRY")
    exit_coord = _parse_coordinate(raw_values["EXIT"], "EXIT")

    if entry == exit_coord:
        raise MazeConfigError("ENTRY and EXIT cannot share the same coordinate"
                              )
    if not _coord_in_bounds(entry, width, height):
        raise MazeConfigError("ENTRY coordinate is outside the defined maze "
                              "boundaries.")
    if not _coord_in_bounds(exit_coord, width, height):
        raise MazeConfigError("EXIT coordinate is outside the defined maze "
                              "boundaries.")

    output_file = Path(raw_values["OUTPUT_FILE"])
    if not output_file.name:
        raise MazeConfigError("OUTPUT_FILE path cannot be completely empty.")

    perfect = _parse_bool(raw_values["PERFECT"], "PERFECT")
    if not perfect:
        raise MazeConfigError("The current generator implementation only "
                              "supports PERFECT=True.")

    seed_value = raw_values.get("SEED")
    seed: int | str | None = seed_value
    if seed_value is not None:
        try:
            seed = int(seed_value)
        except ValueError:
            pass  # Fallback to string if it cannot be cast to an integer

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_coord,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )


def _parse_positive_int(value: str, key: str) -> int:
    """Safely convert a string to a strictly positive integer."""

    try:
        parsed_value = int(value)
    except ValueError as error:
        raise MazeConfigError(f"'{key}' must be a valid integer.") from error

    if parsed_value <= 0:
        raise MazeConfigError(f"'{key}' must be strictly greater than zero.")

    return parsed_value


def _parse_coordinate(value: str, key: str) -> Coordinate:
    """Extract a zero-based `x,y` coordinate pair from a comma-separated
    string."""

    try:
        x_str, y_str = value.split(",")
        return Coordinate(x=int(x_str.strip()), y=int(y_str.strip()))
    except ValueError as error:
        # Catches both tuple unpacking errors and int conversion errors
        raise MazeConfigError(
            f"'{key}' must be a valid integer coordinate pair formatted as "
            f"'x,y'."
        ) from error


def _parse_bool(value: str, key: str) -> bool:
    """Evaluate a string as a boolean value."""

    match value.strip().lower():
        case "true":
            return True
        case "false":
            return False
        case _:
            raise MazeConfigError(f"'{key}' must be explicitly 'True' or "
                                  f"'False'.")


def _coord_in_bounds(coord: Coordinate, width: int, height: int) -> bool:
    """Validate if a given coordinate falls within the rectangular grid
    dimensions."""

    return 0 <= coord.x < width and 0 <= coord.y < height
