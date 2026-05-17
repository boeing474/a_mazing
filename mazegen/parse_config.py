"""Configuration parser and validator."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from .model import Coordinate


class MazeConfigError(Exception):
    """Custom exception raised when configuration is invalid."""
    pass


@dataclass
class MazeConfig:
    """Strongly typed configuration data."""
    width: int
    height: int
    entry: Coordinate
    exit: Coordinate
    output_file: str
    perfect: bool
    seed: Optional[int] = None  # Opcional, usado pelo generator.py


def parse_bool(value: str) -> bool:
    """Parses a string into a boolean safely."""
    val = value.strip().lower()
    if val in ("true", "1", "yes", "t", "sim"):
        return True
    if val in ("false", "0", "no", "f", "nao", "não"):
        return False
    raise MazeConfigError(f"Invalid boolean value for PERFECT: '{value}'")


def parse_coord(value: str) -> Coordinate:
    """Parses a 'x,y' string into a Coordinate."""
    parts = value.split(",")
    if len(parts) != 2:
        raise MazeConfigError(
            f"Invalid coordinate format (expected 'x,y'): '{value}'"
        )
    try:
        return Coordinate(int(parts[0].strip()), int(parts[1].strip()))
    except ValueError:
        raise MazeConfigError(
            f"Coordinate values must be integers: '{value}'"
        )


def load_config(file_path: str) -> MazeConfig:
    """Reads, parses, and validates the config file."""
    if not os.path.exists(file_path):
        raise MazeConfigError(
            f"The configuration file '{file_path}' was not found."
        )

    try:
        # Uso de context manager obrigatório para evitar leaks
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        raise MazeConfigError(f"Error reading file '{file_path}': {e}")

    raw_config: dict[str, str] = {}
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        # O subject exige ignorar linhas vazias e comentários com '#'
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            raise MazeConfigError(
                f"Invalid format on line {line_num}: '{line}' (Missing '=')"
            )

        key, value = line.split("=", 1)
        raw_config[key.strip().upper()] = value.strip()

    # Validação de chaves obrigatórias
    required_keys = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                     "PERFECT"}
    missing_keys = required_keys - raw_config.keys()
    if missing_keys:
        raise MazeConfigError(
            f"Missing required configuration keys: {', '.join(missing_keys)}"
        )

    # Conversão de tipos segura
    try:
        width = int(raw_config["WIDTH"])
        height = int(raw_config["HEIGHT"])

        if width <= 0 or height <= 0:
            raise MazeConfigError("WIDTH and HEIGHT must be positive integers."
                                  )

        entry = parse_coord(raw_config["ENTRY"])
        exit_coord = parse_coord(raw_config["EXIT"])
        output_file = raw_config["OUTPUT_FILE"]
        perfect = parse_bool(raw_config["PERFECT"])

        seed = int(raw_config["SEED"]) if "SEED" in raw_config else None

        return MazeConfig(
            width=width,
            height=height,
            entry=entry,
            exit=exit_coord,
            output_file=output_file,
            perfect=perfect,
            seed=seed
        )
    except ValueError as e:
        raise MazeConfigError(f"Type conversion error in configuration: {e}")
