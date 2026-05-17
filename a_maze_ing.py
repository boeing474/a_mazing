import sys
import parse_config
import maze_generator


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <ficheiro_de_configuracao>")
        sys.exit(1)

    file_name = sys.argv[1]

    parsed_config = parse_config.load(file_name)

    print("Configs loaded successfully:")
    print(parsed_config)

    qnt_cells = int(parsed_config["WIDTH"]) * int(parsed_config["HEIGHT"]) # parseando na forca aqui só pra testar.
    
    # logica de geracao do labirinto
    maze = maze_generator.MazeGenerator()
    maze.generate_grid(qnt_cells)


if __name__ == "__main__":
    main()
