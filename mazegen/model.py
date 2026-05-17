"""Main data structures used by the genarator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class Direction(IntEnum):
    """Cardinal directions mapped to the subject hexadecimal wall bits."""

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    @property
    def delta(self) -> tuple[int, int]:
        """Return the coordinate delta for this direction."""

        deltas = {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0),
        }
        return deltas[self]

    @property
    def opposite(self) -> "Direction":
        """Return the opposite direction."""

        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.EAST: Direction.WEST,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
        }
        return opposites[self]

    @property
    def symbol(self) -> str:
        """Return the single-letter direction symbol."""

        symbols = {
            Direction.NORTH: "N",
            Direction.EAST: "E",
            Direction.SOUTH: "S",
            Direction.WEST: "W",
        }
        return symbols[self]

    @classmethod
    def ordered(cls) -> tuple["Direction", ...]:
        """Return directions in the subject bit order."""

        return (cls.NORTH, cls.EAST, cls.SOUTH, cls.WEST)


@dataclass(frozen=True)
class Coordinate:
    """Zero-based coordinate inside the maze grid."""

    x: int
    y: int

    def moved(self, direction: Direction) -> "Coordinate":
        """Return the adjacent coordinate in the given direction."""

        dx, dy = direction.delta
        return Coordinate(self.x + dx, self.y + dy)


@dataclass
class Cell:
    """A single maze cell encoded as a 4-bit wall mask."""

    walls: int = 0xF

    def has_wall(self, direction: Direction) -> bool:
        """Return whether the wall is closed in the given direction."""

        return bool(self.walls & int(direction))

    def open_wall(self, direction: Direction) -> None:
        """Remove a wall in the given direction."""

        self.walls &= ~int(direction)


class Maze:
    """Mutable maze grid with coherent wall operations."""

    def __init__(self, width: int, height: int) -> None:
        """Create a maze filled with closed walls."""

        self.width = width
        self.height = height
        self._cells = [Cell() for _ in range(width * height)]

    def in_bounds(self, coord: Coordinate) -> bool:
        """Return whether the coordinate belongs to this maze."""

        return 0 <= coord.x < self.width and 0 <= coord.y < self.height

    def cell_at(self, coord: Coordinate) -> Cell:
        """Return the cell at the given coordinate."""

        return self._cells[coord.y * self.width + coord.x]

    def neighbors(
        self,
        coord: Coordinate,
    ) -> list[tuple[Direction, Coordinate]]:
        """Return in-bounds neighbor coordinates around a cell."""

        result: list[tuple[Direction, Coordinate]] = []
        for direction in Direction.ordered():
            neighbor = coord.moved(direction)
            if self.in_bounds(neighbor):
                result.append((direction, neighbor))
        return result

    def carve_passage(self, origin: Coordinate, direction: Direction) -> None:
        """Open a passage between adjacent cells."""

        target = origin.moved(direction)
        if not self.in_bounds(origin) or not self.in_bounds(target):
            raise ValueError("Cannot carve passage outside maze bounds.")
        self.cell_at(origin).open_wall(direction)
        self.cell_at(target).open_wall(direction.opposite)

    def is_open(self, origin: Coordinate, direction: Direction) -> bool:
        """Return whether a move is possible from one cell to its neighbor."""

        target = origin.moved(direction)
        if not self.in_bounds(target):
            return False
        return not self.cell_at(origin).has_wall(direction)

    def iter_coordinates(self) -> list[Coordinate]:
        """Return all maze coordinates in row order."""

        return [
            Coordinate(x, y)
            for y in range(self.height)
            for x in range(self.width)
        ]
