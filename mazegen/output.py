"""Serialization utilities for exporting maze data to the standard project
format."""

from __future__ import annotations

from pathlib import Path

from .model import Coordinate, Maze


def build_output_text(
    maze: Maze,
    entry: Coordinate,
    exit_coord: Coordinate,
    path_directions: str,
) -> str:
    """Construct the standardized string representation of the maze and its
    metadata."""

    # Generate the hexadecimal representation of the walls for each row
    grid_rows = [
        "".join(
            f"{maze.cell_at(Coordinate(x, y)).walls:X}"
            for x in range(maze.width)
        )
        for y in range(maze.height)
    ]

    # Append the required metadata (blank line, entry, exit, and solution path)
    metadata = [
        "",
        f"{entry.x},{entry.y}",
        f"{exit_coord.x},{exit_coord.y}",
        path_directions,
    ]

    return "\n".join(grid_rows + metadata) + "\n"


def write_output_file(path: Path, contents: str) -> None:
    """Save the serialized maze content to the filesystem, creating
    directories if needed."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")
