import sys
import parse_config


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <ficheiro_de_configuracao>")
        sys.exit(1)

    file_name = sys.argv[1]

    parsed_config = parse_config.load(file_name)

    print("Configs loaded successfully:")
    print(parsed_config)


if __name__ == "__main__":
    main()
