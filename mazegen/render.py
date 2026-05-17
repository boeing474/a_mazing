"""ASCII rendering helpers for terminal output."""

from __future__ import annotations

from .internal42 import get_42_pattern_cells
from .model import Coordinate, Direction, Maze


# ANSI color codes for terminal output
RESET_COLOR = "\033[0m"
ENTRY_COLOR = "\033[32m"     # Green
EXIT_COLOR = "\033[31m"      # Red
PATH_COLOR = "\033[33m"      # Yellow
PATTERN_COLOR = "\033[35m"   # Magenta


def render_ascii(
    maze: Maze,
    entry: Coordinate,
    exit_coord: Coordinate,
    solution: list[Coordinate],
    wall_color: str = "",
) -> str:
    """Render the maze with solid walls, entry, exit, and solution path."""
    solution_cells = set(solution[1:-1])
    pattern_cells = get_42_pattern_cells(
        maze.width,
        maze.height,
        entry,
        exit_coord,
    )
    lines: list[str] = []

    # Top of the maze
    top = _wall("██", wall_color)
    for x in range(maze.width):
        top += (
            _wall("████", wall_color)
            if maze.cell_at(Coordinate(x, 0)).has_wall(Direction.NORTH)
            else f"  {_wall('██', wall_color)}"
        )
    lines.append(top)

    # Body of the maze
    for y in range(maze.height):
        middle = ""
        bottom = _wall("██", wall_color)

        for x in range(maze.width):
            coord = Coordinate(x, y)
            cell = maze.cell_at(coord)

            # West wall (2 chars)
            middle += (
                _wall("██", wall_color)
                if cell.has_wall(Direction.WEST)
                else "  "
            )

            # Cell interior filled with colors and solid blocks
            middle += _cell_marker(
                coord,
                entry,
                exit_coord,
                solution_cells,
                pattern_cells,
            )

            # South wall (covers the cell and connects to
            # the next pillar = 4 chars)
            bottom += (
                _wall("████", wall_color)
                if cell.has_wall(Direction.SOUTH)
                else f"  {_wall('██', wall_color)}"
            )

        # East wall (closes the last cell of the row)
        middle += (
            _wall("██", wall_color)
            if maze.cell_at(
                Coordinate(maze.width - 1, y)
            ).has_wall(Direction.EAST)
            else "  "
        )

        lines.append(middle)
        lines.append(bottom)

    return "\n".join(lines)


def _cell_marker(
    coord: Coordinate,
    entry: Coordinate,
    exit_coord: Coordinate,
    solution_cells: set[Coordinate],
    pattern_cells: set[Coordinate],
) -> str:
    """Return the colored solid blocks used to display interactive elements."""
    if coord == entry:
        return f"{ENTRY_COLOR}██{RESET_COLOR}"
    if coord == exit_coord:
        return f"{EXIT_COLOR}██{RESET_COLOR}"
    if coord in pattern_cells:
        return f"{PATTERN_COLOR}██{RESET_COLOR}"
    if coord in solution_cells:
        return f"{PATH_COLOR}██{RESET_COLOR}"

    return "  "


def _wall(token: str, wall_color: str) -> str:
    """Return a wall token optionally with ANSI color codes."""
    if not wall_color:
        return token
    return f"{wall_color}{token}{RESET_COLOR}"
