"""Validate de maze and finds the shortest path"""

from __future__ import annotations

from collections import deque

from .model import Coordinate, Direction, Maze
from .internal42 import get_42_pattern_cells


class MazeValidationError(Exception):
    """Raised when a generated maze violates a mandatory rule."""


def validate_maze(
    maze: Maze,
    entry: Coordinate,
    exit_coord: Coordinate,
    perfect: bool,
) -> None:
    """Validate structural maze constraints used by the project."""

    pattern_cells = get_42_pattern_cells(
        maze.width,
        maze.height,
        entry,
        exit_coord,
    )
    if not maze.in_bounds(entry):
        raise MazeValidationError("Entry coordinate is outside the maze.")
    if not maze.in_bounds(exit_coord):
        raise MazeValidationError("Exit coordinate is outside the maze.")
    _validate_42_pattern_cells(maze, pattern_cells)
    _validate_neighbor_coherence(maze)
    _validate_borders(maze)
    if not _is_fully_connected(maze, pattern_cells):
        raise MazeValidationError("Maze is not fully connected.")
    if _has_open_three_by_three_area(maze):
        raise MazeValidationError("Maze contains a forbidden 3x3 open area.")
    if perfect and not _is_tree(maze, pattern_cells):
        raise MazeValidationError(
            "PERFECT=True requires exactly one path between any two cells."
        )
    _, directions = solve_shortest_path(maze, entry, exit_coord)
    if not directions and entry != exit_coord:
        raise MazeValidationError(
            "Maze has no valid path between entry and exit."
        )


def solve_shortest_path(
    maze: Maze,
    entry: Coordinate,
    exit_coord: Coordinate,
) -> tuple[list[Coordinate], str]:
    """Return the shortest path as coordinates and N/E/S/W directions."""

    queue: deque[Coordinate] = deque([entry])
    previous: dict[Coordinate, tuple[Coordinate, Direction] | None] = {
        entry: None
    }

    while queue:
        current = queue.popleft()
        if current == exit_coord:
            break
        for direction, neighbor in maze.neighbors(current):
            if neighbor in previous:
                continue
            if not maze.is_open(current, direction):
                continue
            previous[neighbor] = (current, direction)
            queue.append(neighbor)

    if exit_coord not in previous:
        return [], ""

    coordinates: list[Coordinate] = []
    direction_steps: list[str] = []
    current = exit_coord
    while current != entry:
        coordinates.append(current)
        previous_item = previous[current]
        if previous_item is None:
            break
        parent, direction = previous_item
        direction_steps.append(direction.symbol)
        current = parent
    coordinates.append(entry)
    coordinates.reverse()
    direction_steps.reverse()
    return coordinates, "".join(direction_steps)


def _validate_neighbor_coherence(maze: Maze) -> None:
    """Ensure adjacent cells agree on whether a shared wall is open."""

    for coord in maze.iter_coordinates():
        for direction, neighbor in maze.neighbors(coord):
            current_open = maze.is_open(coord, direction)
            neighbor_open = maze.is_open(neighbor, direction.opposite)
            if current_open != neighbor_open:
                raise MazeValidationError(
                    "Neighboring cells disagree about a wall."
                )


def _validate_42_pattern_cells(
    maze: Maze,
    pattern_cells: set[Coordinate],
) -> None:
    """Ensure reserved 42 cells remain fully closed."""

    for coord in pattern_cells:
        if maze.cell_at(coord).walls != 0xF:
            raise MazeValidationError(
                "42 pattern cells must remain fully closed."
            )


def _validate_borders(maze: Maze) -> None:
    """Ensure the external border remains closed."""

    for x in range(maze.width):
        if not maze.cell_at(Coordinate(x, 0)).has_wall(Direction.NORTH):
            raise MazeValidationError("Top border must stay closed.")
        if not maze.cell_at(
            Coordinate(x, maze.height - 1)
        ).has_wall(Direction.SOUTH):
            raise MazeValidationError("Bottom border must stay closed.")
    for y in range(maze.height):
        if not maze.cell_at(Coordinate(0, y)).has_wall(Direction.WEST):
            raise MazeValidationError("Left border must stay closed.")
        if not maze.cell_at(
            Coordinate(maze.width - 1, y)
        ).has_wall(Direction.EAST):
            raise MazeValidationError("Right border must stay closed.")


def _is_fully_connected(maze: Maze, pattern_cells: set[Coordinate]) -> bool:
    """Return whether every non-pattern cell can be reached."""

    active_cells = [
        coord
        for coord in maze.iter_coordinates()
        if coord not in pattern_cells
    ]
    if not active_cells:
        return False

    start = active_cells[0]
    queue: deque[Coordinate] = deque([start])
    visited = {start}

    while queue:
        current = queue.popleft()
        for direction, neighbor in maze.neighbors(current):
            if neighbor in visited or neighbor in pattern_cells:
                continue
            if not maze.is_open(current, direction):
                continue
            visited.add(neighbor)
            queue.append(neighbor)

    return len(visited) == len(active_cells)


def _is_tree(maze: Maze, pattern_cells: set[Coordinate]) -> bool:
    """Return whether the active maze graph is a spanning tree."""

    undirected_edges = 0
    for coord in maze.iter_coordinates():
        if coord in pattern_cells:
            continue
        for direction in (Direction.EAST, Direction.SOUTH):
            neighbor = coord.moved(direction)
            if neighbor in pattern_cells:
                continue
            if maze.is_open(coord, direction):
                undirected_edges += 1
    node_count = sum(
        1 for coord in maze.iter_coordinates() if coord not in pattern_cells
    )
    return (
        _is_fully_connected(maze, pattern_cells)
        and undirected_edges == node_count - 1
    )


def _has_open_three_by_three_area(maze: Maze) -> bool:
    """Detect fully open 3x3 blocks with no internal walls."""

    if maze.width < 3 or maze.height < 3:
        return False
    for start_y in range(maze.height - 2):
        for start_x in range(maze.width - 2):
            fully_open = True
            for y in range(start_y, start_y + 3):
                for x in range(start_x, start_x + 2):
                    if not maze.is_open(Coordinate(x, y), Direction.EAST):
                        fully_open = False
                        break
                if not fully_open:
                    break
            if not fully_open:
                continue
            for y in range(start_y, start_y + 2):
                for x in range(start_x, start_x + 3):
                    if not maze.is_open(Coordinate(x, y), Direction.SOUTH):
                        fully_open = False
                        break
                if not fully_open:
                    break
            if fully_open:
                return True
    return False
