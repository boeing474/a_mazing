"""Maze generation algorithms."""

from __future__ import annotations

import random

from .parse_config import MazeConfig
from .model import Maze
from .pattern import get_42_pattern_cells


class MazeGenerator:
    """Generate a maze using a seeded recursive-backtracking strategy."""

    def __init__(self, config: MazeConfig) -> None:
        """Store generator settings and initialize deterministic randomness."""

        self.config = config
        self._random = random.Random(config.seed)

    def generate(self) -> Maze:
        """Generate a maze that satisfies the mandatory perfect-maze rules."""

        return self._generate_perfect_maze()

    def _generate_perfect_maze(self) -> Maze:
        """Build a perfect maze with iterative recursive backtracking."""

        maze = Maze(self.config.width, self.config.height)
        pattern_cells = get_42_pattern_cells(
            self.config.width,
            self.config.height,
            self.config.entry,
            self.config.exit,
        )
        active_cells = [
            coord
            for coord in maze.iter_coordinates()
            if coord not in pattern_cells
        ]
        if not active_cells:
            raise ValueError(
                "Maze does not contain any active cells to generate."
            )

        start = self._random.choice(active_cells)
        stack = [start]
        visited = {start}

        while stack:
            current = stack[-1]
            candidates = [
                (direction, neighbor)
                for direction, neighbor in maze.neighbors(current)
                if neighbor not in visited and neighbor not in pattern_cells
            ]
            if not candidates:
                stack.pop()
                continue

            direction, neighbor = self._random.choice(candidates)
            maze.carve_passage(current, direction)
            visited.add(neighbor)
            stack.append(neighbor)

        return maze
