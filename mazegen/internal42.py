"""Helper for putting the internal 42."""

from __future__ import annotations

from .model import Coordinate


PATTERN_ROWS = (
    "1010111",
    "1010001",
    "1110111",
    "0010100",
    "0010111",
)


def get_42_pattern_minimum_size() -> tuple[int, int]:
    """Return the minimum maze size required to place the 42 pattern."""

    pattern_height = len(PATTERN_ROWS)
    pattern_width = len(PATTERN_ROWS[0])
    return pattern_width + 2, pattern_height + 2


def can_fit_42_pattern(width: int, height: int) -> bool:
    """Return whether the maze dimensions allow the 42 pattern."""

    minimum_width, minimum_height = get_42_pattern_minimum_size()
    return width >= minimum_width and height >= minimum_height


def get_42_pattern_cells(
    width: int,
    height: int,
    entry: Coordinate,
    exit_coord: Coordinate,
) -> set[Coordinate]:
    """Return reserved cells used to draw the 42 pattern when space allows."""

    pattern_height = len(PATTERN_ROWS)
    pattern_width = len(PATTERN_ROWS[0])
    if not can_fit_42_pattern(width, height):
        return set()

    placements = [
        Coordinate(x=left, y=top)
        for top in range(1, height - pattern_height)
        for left in range(1, width - pattern_width)
    ]
    placements.sort(
        key=lambda coord: (
            abs((coord.x + pattern_width / 2) - (width / 2)),
            abs((coord.y + pattern_height / 2) - (height / 2)),
        )
    )

    for top_left in placements:
        cells = _build_pattern_cells(top_left)
        if entry in cells or exit_coord in cells:
            continue
        return cells
    return set()


def _build_pattern_cells(top_left: Coordinate) -> set[Coordinate]:
    """Build pattern coordinates from the bitmap definition."""

    cells: set[Coordinate] = set()
    for row_index, row in enumerate(PATTERN_ROWS):
        for column_index, value in enumerate(row):
            if value != "1":
                continue
            cells.add(
                Coordinate(
                    x=top_left.x + column_index,
                    y=top_left.y + row_index,
                )
            )
    return cells
