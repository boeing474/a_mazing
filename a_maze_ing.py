"""CLI entry point for the A-Maze-ing application."""

from __future__ import annotations

from dataclasses import replace
import sys

from mazegen import (
    Coordinate,
    Maze,
    MazeConfig,
    MazeConfigError,
    MazeGenerator,
    MazeValidationError,
    load_config,
    solve_shortest_path,
    validate_maze,
)
from mazegen.output import build_output_text, write_output_file
from mazegen.pattern import can_fit_42_pattern, get_42_pattern_minimum_size
from mazegen.render import render_ascii

ANSI_CLEAR_SCREEN = "\033[2J\033[H"
WALL_COLORS = (
    ("Default", ""),
    ("Blue", "\033[34m"),
    ("Green", "\033[1;32m"),
    ("Yellow", "\033[33m"),
    ("Cyan", "\033[36m"),
    ("Magenta", "\033[35m"),
)


def main(argv: list[str] | None = None) -> int:
    """Execute the maze generator application from the terminal."""
    
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        return 1

    try:
        initial_config = load_config(args[0])
        _run_interactive_session(initial_config)
        return 0
    except KeyboardInterrupt:
        print()
        return 130
    except (MazeConfigError, MazeValidationError, ValueError, OSError) as error:
        print(f"Application Error: {error}", file=sys.stderr)
        return 1
    except Exception as error:  # pragma: no cover
        print(f"Critical System Error: {error}", file=sys.stderr)
        return 1


def _run_interactive_session(config: MazeConfig) -> None:
    """Manage the interactive ASCII rendering and handle user inputs."""
    
    display_path = True
    color_idx = 0
    gen_count = 0
    feedback_msg = ""
    pattern_warning = _check_42_pattern_compatibility(config)
    
    # Initialize the first maze state
    active_config = config
    maze, solution_path, path_str = _process_maze_lifecycle(active_config)

    while True:
        color_label, ansi_code = WALL_COLORS[color_idx]
        print(ANSI_CLEAR_SCREEN, end="")
        
        active_solution = solution_path if display_path else []
        
        print(
            render_ascii(
                maze,
                active_config.entry,
                active_config.exit,
                active_solution,
                ansi_code,
            )
        )
        
        print(f"\nSuccessfully exported to: {active_config.output_file}")
        print(f"Path solution: {path_str if display_path else '[Hidden]'}")
        print(
            f"Commands: [r] Regen  |  [p] Toggle Path  |  "
            f"[c] Color ({color_label})  |  [q] Exit"
        )
        
        if pattern_warning:
            print(pattern_warning)
        if feedback_msg:
            print(feedback_msg)
            
        try:
            user_input = input("Action: ").strip().lower()
        except EOFError:
            print()
            break

        feedback_msg = ""
        
        match user_input:
            case "q" | "quit":
                break
                
            case "p" | "path":
                display_path = not display_path
                state_label = "ON" if display_path else "OFF"
                feedback_msg = f"Path visibility is now {state_label}."
                
            case "c" | "color" | "colour":
                color_idx = (color_idx + 1) % len(WALL_COLORS)
                new_color = WALL_COLORS[color_idx][0]
                feedback_msg = f"Active color updated to {new_color}."
                
            case "r" | "regen" | "regenerate":
                gen_count += 1
                active_config = _derive_next_config(config, gen_count)
                maze, solution_path, path_str = _process_maze_lifecycle(active_config)
                feedback_msg = "Maze successfully regenerated."
                
            case _:
                feedback_msg = "Invalid input. Please choose r, p, c, or q."


def _process_maze_lifecycle(
    config: MazeConfig,
) -> tuple[Maze, list[Coordinate], str]:
    """Create, validate, solve, and save a maze based on the provided configuration."""
    
    maze_gen = MazeGenerator(config)
    generated_maze = maze_gen.generate()
    
    validate_maze(
        generated_maze,
        config.entry,
        config.exit,
        config.perfect,
    )
    
    path_cells, path_string = solve_shortest_path(
        generated_maze,
        config.entry,
        config.exit,
    )
    
    file_content = build_output_text(
        generated_maze,
        config.entry,
        config.exit,
        path_string,
    )
    write_output_file(config.output_file, file_content)
    
    return generated_maze, path_cells, path_string


def _derive_next_config(
    base_config: MazeConfig,
    iteration: int,
) -> MazeConfig:
    """Create a new configuration object with an updated seed for regeneration."""
    
    if iteration == 0:
        return base_config
        
    current_seed = base_config.seed if base_config.seed is not None else "interactive"
    return replace(base_config, seed=f"{current_seed}:regen:{iteration}")


def _check_42_pattern_compatibility(config: MazeConfig) -> str:
    """Construct a warning message if the maze dimensions cannot accommodate the 42 pattern."""
    
    if can_fit_42_pattern(config.width, config.height):
        return ""
        
    min_w, min_h = get_42_pattern_minimum_size()
    return (
        f"Note: The 42 pattern was skipped. Current size ({config.width}x{config.height}) "
        f"does not meet the minimum requirement ({min_w}x{min_h})."
    )


if __name__ == "__main__":
    sys.exit(main())
