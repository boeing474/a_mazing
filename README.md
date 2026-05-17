_This project has been created as part of the 42 curriculum by ramrodri and pboeing-_

# A-Maze-ing

## Description

`A-Maze-ing` is a robust, Python 3.10+ based maze generator designed for the 42 curriculum. Its primary objective is to read and validate a configuration file, procedurally generate a maze that adheres strictly to mandatory rules, and determine the shortest path from entry to exit. Finally, it provides a highly visual, proportion-corrected ASCII render in the terminal and exports the grid data in the requested hexadecimal format.

The architecture is split into a standalone, reusable core package called [`mazegen/`](https://www.google.com/search?q=/home/glopes-a/a-maze-ing/mazegen) and a command-line interface entry point, [`a_maze_ing.py`](https://www.google.com/search?q=/home/glopes-a/a-maze-ing/a_maze_ing.py).

The application lifecycle follows these steps:

1. Parse and enforce configuration rules.
2. Generate the maze topology based on the validated parameters.
3. Perform a structural validation on the generated grid.
4. Calculate the shortest escape route using a solving algorithm.
5. Display an upgraded interactive ASCII render with solid ANSI-colored blocks.
6. Serialize and write the hexadecimal output to the target file.

## Instructions

### Requirements

* Python `3.10` or higher
* A standard shell environment with `make` and `python3` available

### Installation

To set up the project locally in editable mode, run:

```bash
make install

```

Alternatively, you can use pip directly:

```bash
python3 -m pip install -e .

```

### Execution

To launch the generator via the main CLI, provide your configuration file as an argument:

```bash
python3 a_maze_ing.py config.txt

```

Or simply trigger the Makefile rule:

```bash
make run

```

Once executed, the application will:

* Process the instructions found in `config.txt`.
* Launch an interactive terminal session displaying the maze.
* Automatically dump the finalized hexadecimal structure into the specified `OUTPUT_FILE`.

### Useful Commands

* `make package`: Compiles a distributable wheel (e.g., `mazegen-0.1.0-py3-none-any.whl`) in the root directory.
* `make debug`: Initializes a debugging session using Python's native `pdb`.
* `make lint`: Executes strict static analysis using `flake8` (PEP 8 compliance) and `mypy`.
* `python3 -m build`: Regenerates package artifacts inside the `dist/` folder.
* `python3 tools/validate_sample.py`: Triggers a quick test generation and outputs a validation summary.

## Configuration File

The engine reads a simple text file structured as `KEY=VALUE` pairs.

Parsing Rules:

* Blank lines and comments (lines starting with `#`) are safely ignored.
* Duplicated parameters will trigger a validation error.
* All mandatory keys must be present.

### File Structure

**Required Keys:**

* `WIDTH`
* `HEIGHT`
* `ENTRY`
* `EXIT`
* `OUTPUT_FILE`
* `PERFECT`

**Optional Keys:**

* `SEED`

### Formatting Constraints

* `WIDTH=<positive integer>`
* `HEIGHT=<positive integer>`
* `ENTRY=<x,y>`
* `EXIT=<x,y>`
* `OUTPUT_FILE=<valid path or filename>`
* `PERFECT=True|False`
* `SEED=<integer or string>` (optional)

**Hardcoded Business Rules:**

* Both `ENTRY` and `EXIT` rely on a 0-based coordinate system.
* `ENTRY` and `EXIT` must fall strictly within the grid dimensions.
* `ENTRY` and `EXIT` cannot share the same position.
* The `OUTPUT_FILE` string cannot be empty.
* As of the current version, the engine exclusively supports `PERFECT=True`.

### Example config.txt

```text
# Default A-Maze-ing configuration
WIDTH=15
HEIGHT=13
ENTRY=0,0
EXIT=10,5
OUTPUT_FILE=output_maze.txt
PERFECT=True
SEED=42

```

## Generation Algorithm

At its core, the engine relies on a seeded **recursive backtracking algorithm**. To ensure stability on massive grids, it is implemented iteratively using an explicit stack rather than standard Python recursion, preventing depth-limit exceptions. This logic resides in [`mazegen/generator.py`](https://www.google.com/search?q=/home/glopes-a/a-maze-ing/mazegen/generator.py).

**How it works:**

1. Initialize a fully enclosed grid where every cell has all walls intact (mask `0xF`).
2. If the dimensions permit, reserve a specific cluster of cells for the internal `42` pattern.
3. Select a random starting cell dictated by the provided `SEED`.
4. Randomly pick an unvisited neighboring cell.
5. Carve a path by knocking down the shared wall between the current cell and the chosen neighbor.
6. Push the neighbor onto the tracking stack and move forward.
7. If a dead-end is reached (no unvisited neighbors), pop the stack to backtrack.
8. The process concludes once every accessible cell has been visited.

### Why Recursive Backtracking?

This approach perfectly aligns with the project's strict constraints:

* It inherently builds a spanning tree, guaranteeing a fully connected maze (ideal for `PERFECT=True`).
* It is highly predictable and works seamlessly with deterministic PRNG seeds.
* It is elegant to implement and integrates beautifully with our bitwise wall logic.
* Using an explicit stack guarantees it won't crash on huge dimensions, making debugging much smoother.

## Maze Format And Model

To maximize performance and minimize memory footprint, the project utilizes `slots=True` data classes and `match/case` Enum structures. Each cell tracks its boundaries using a highly efficient 4-bit bitmask defined in [`mazegen/model.py`](https://www.google.com/search?q=/home/glopes-a/a-maze-ing/mazegen/model.py):

* `1`: North wall
* `2`: East wall
* `4`: South wall
* `8`: West wall

By default, a cell starts at `0xF` (binary `1111`, fully walled). As the generator carves paths, it applies bitwise operations to update the walls bidirectionally.

Key architectural types:

* `Direction`: Enumeration of cardinal points featuring coordinate delta properties.
* `Coordinate`: Highly optimized, immutable `(x, y)` pairings.
* `Cell`: The atomic unit of the maze holding the wall state.
* `Maze`: The main grid orchestrator managing bounding logic and neighbor traversal.

## Output Format

The output artifact is generated line by line, mapping each cell to its corresponding hexadecimal wall value. Following a blank line, a crucial metadata block is appended.

This block contains:

1. The entry coordinates.
2. The exit coordinates.
3. A string representing the shortest route to the exit.

This rigidly matches the `x,y \n x,y \n NNEESW` specification required by the 42 evaluation scale.

**Example Export:**

```text
97953953
C56BC6BA
9552952A
A956C3C6
AC393A93
C7C6C46E

0,0
7,5
SEENEESENEESSSWNWWSESSENES

```

## Reusable Parts

One of the project's major strengths is its modularity. The core logic is isolated within the [`mazegen/`](https://www.google.com/search?q=/home/glopes-a/a-maze-ing/mazegen) package, meaning the generator can be imported and utilized independently of the provided CLI tool.

**Module Breakdown:**

* [`mazegen/config.py`](https://www.google.com/search?q=/home/glopes-a/a-maze-ing/mazegen/config.py): Parser and strict constraint validator.
* [`mazegen/model.py`](https://www.google.com/search?q=/home/glopes-a/a-maze-ing/mazegen/model.py): Core data structures (`Maze`, `Cell`, `Coordinate`).
* [`mazegen/generator.py`](https://www.google.com/search?q=/home/glopes-a/a-maze-ing/mazegen/generator.py): The backtracking engine.
* [`mazegen/solver.py`](https://www.google.com/search?q=/home/glopes-a/a-maze-ing/mazegen/solver.py): Breadth-first search for pathfinding and topology validation.
* [`mazegen/render.py`](https://www.google.com/search?q=/home/glopes-a/a-maze-ing/mazegen/render.py): Terminal UI using double-width ANSI solid blocks for correct aspect ratio.
* [`mazegen/output.py`](https://www.google.com/search?q=/home/glopes-a/a-maze-ing/mazegen/output.py): Hexadecimal serialization logic.

## Team And Project Management

### Team Roles

* **`glopes-a`**: Focused on software architecture, packaging, CLI integration, and technical documentation.
* **`vguerra-`**: Driven by algorithm implementation, validation constraints, unit checks, and structural reviews.

*Note: The development process was highly fluid, with both contributors actively reviewing pull requests, discussing architectural decisions, and refining output compliance.*

### Planning and Evolution

**Initial Roadmap:**

1. Establish the bitwise grid model.
2. Build the configuration parser.
3. Implement the core generation algorithm.
4. Integrate the shortest-path solver.
5. Create terminal visuals and file exporters.
6. Package the application and draft documentation.

**How it Adapted:**

* The distinction between the CLI and the underlying package became a priority, leading to a much cleaner architecture.
* Validation scaled up significantly. What started as basic boundary checks evolved into complex topology verification (detecting loops, isolated areas, and `3x3` open spaces).
* The visual rendering was entirely refactored to use solid ANSI blocks (`██`), effectively fixing terminal aspect ratio distortions and delivering a polished UI.

### Successes

* Decoupling the CLI from the `mazegen/` library made the codebase highly maintainable.
* The 4-bit wall encoding proved to be incredibly fast and reliable for both generation and export.
* Applying modern Python features (`match/case`, `frozensets`, slotted dataclasses) yielded excellent performance.

### Future Improvements

* While `PERFECT=True` is flawlessly executed, implementing non-perfect generation (e.g., adding deliberate loops) is the logical next step.
* Expanding automated unit tests beyond the current manual and linting workflows.

### Toolkit

* `Python 3.10+`
* `make`
* `flake8` (Code styling)
* `mypy` (Static type checking)

## Validation And Quality Checks

To manually ensure application stability, the following workflow is recommended:

```bash
python3 a_maze_ing.py config.txt
python3 tools/validate_sample.py
make lint

```

**Testing Scenarios:**

* Delete a mandatory key from `config.txt`.
* Supply an invalid `ENTRY` outside the matrix dimensions.
* Map `ENTRY` and `EXIT` to the exact same spot.
* Modify the `SEED` and verify grid mutations.
* Keep the `SEED` static across executions to prove deterministic generation.

## Advanced Features

While satisfying all mandatory requirements, this version ships with several advanced capabilities:

* **Deterministic Mutability:** Reliable seed-based generation.
* **Visual Overhaul:** An interactive CLI that renders proportional, solid-block mazes with dynamic ANSI color themes.
* **Topology Auditing:** Comprehensive post-generation checks ensuring the maze is mathematically perfect.
* **Easter Egg:** Automatic embedding and coloring of the `42` pattern when the dimensions allow for it.

## Resources

Key documentation and algorithms referenced during development:

* Python Official Docs: [https://docs.python.org/3/](https://docs.python.org/3/)
* Dataclasses: [https://docs.python.org/3/library/dataclasses.html](https://docs.python.org/3/library/dataclasses.html)
* Enums: [https://docs.python.org/3/library/enum.html](https://docs.python.org/3/library/enum.html)
* Pathlib: [https://docs.python.org/3/library/pathlib.html](https://docs.python.org/3/library/pathlib.html)
* Recursive Backtracking: [https://en.wikipedia.org/wiki/Maze_generation_algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
* BFS Pathfinding: [https://en.wikipedia.org/wiki/Breadth-first_search](https://en.wikipedia.org/wiki/Breadth-first_search)

### AI Usage

AI tooling was utilized to:

* Polish and restructure this README for better technical clarity.
* Modernize code snippets to leverage Python 3.10 syntax (e.g., `match/case`).
* Refine terminal visual algorithms to fix aspect ratio clipping.