"""Main core data structures used by the maze generator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class Direction(IntEnum):
    """Cardinal directions mapped to their respective hexadecimal wall bits."""

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    @property
    def delta(self) -> tuple[int, int]:
        """Return the (dx, dy) coordinate delta for this direction."""
        match self:
            case Direction.NORTH:
                return (0, -1)
            case Direction.EAST:
                return (1, 0)
            case Direction.SOUTH:
                return (0, 1)
            case Direction.WEST:
                return (-1, 0)

    @property
    def opposite(self) -> "Direction":
        """Return the strictly opposite cardinal direction."""
        match self:
            case Direction.NORTH:
                return Direction.SOUTH
            case Direction.EAST:
                return Direction.WEST
            case Direction.SOUTH:
                return Direction.NORTH
            case Direction.WEST:
                return Direction.EAST

    @property
    def symbol(self) -> str:
        """Return the single-character representation of the direction."""
        match self:
            case Direction.NORTH:
                return "N"
            case Direction.EAST:
                return "E"
            case Direction.SOUTH:
                return "S"
            case Direction.WEST:
                return "W"

    @classmethod
    def ordered(cls) -> tuple["Direction", ...]:
        """Return directions strictly in their bit order (N, E, S, W)."""
        return tuple(cls)


@dataclass(frozen=True, slots=True)
class Coordinate:
    """Immutable, zero-based Cartesian coordinate inside the maze grid."""

    x: int
    y: int

    def moved(self, direction: Direction) -> "Coordinate":
        """Calculate and return the adjacent coordinate
        in the specified direction."""
        dx, dy = direction.delta
        return Coordinate(self.x + dx, self.y + dy)


@dataclass(slots=True)
class Cell:
    """A single maze cell encoding its four walls
    as a 4-bit bitmask."""

    walls: int = 0xF

    def has_wall(self, direction: Direction) -> bool:
        """Check if the wall in the specified
        direction is closed."""
        return bool(self.walls & direction.value)

    def open_wall(self, direction: Direction) -> None:
        """Destroy the wall in the specified direction."""
        self.walls &= ~direction.value


class Maze:
    """Mutable maze grid handling core topological operations and state."""

    __slots__ = ("width", "height", "_cells")

    def __init__(self, width: int, height: int) -> None:
        """Initialize a fully walled maze of the given dimensions."""
        self.width = width
        self.height = height
        self._cells = [Cell() for _ in range(width * height)]

    def in_bounds(self, coord: Coordinate) -> bool:
        """Verify if a coordinate falls within the grid dimensions."""
        return 0 <= coord.x < self.width and 0 <= coord.y < self.height

    def cell_at(self, coord: Coordinate) -> Cell:
        """Retrieve the Cell object at the specified coordinate."""
        return self._cells[coord.y * self.width + coord.x]

    def neighbors(
        self,
        coord: Coordinate,
    ) -> list[tuple[Direction, Coordinate]]:
        """List all valid, in-bounds adjacent coordinates
        around a given cell."""
        return [
            (direction, coord.moved(direction))
            for direction in Direction
            if self.in_bounds(coord.moved(direction))
        ]

    def carve_passage(self, origin: Coordinate, direction: Direction) -> None:
        """Bidirectionally open a path between two adjacent cells."""
        target = origin.moved(direction)
        if not (self.in_bounds(origin) and self.in_bounds(target)):
            raise ValueError("Cannot carve a passage outside "
                             "the maze boundaries.")

        self.cell_at(origin).open_wall(direction)
        self.cell_at(target).open_wall(direction.opposite)

    def is_open(self, origin: Coordinate, direction: Direction) -> bool:
        """Determine if passage is clear from the origin
        in the given direction."""
        if not self.in_bounds(origin.moved(direction)):
            return False
        return not self.cell_at(origin).has_wall(direction)

    def iter_coordinates(self) -> list[Coordinate]:
        """Generate all grid coordinates sequentially by row."""
        return [
            Coordinate(x, y)
            for y in range(self.height)
            for x in range(self.width)
        ]
