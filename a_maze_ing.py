import sys
import parse_config

def main():
    if len(sys.argv) != 2:
        print("Use: a_maze_ing.py <config_file>")
        sys.exit()

    file_name = sys.argv[1]

    parse_config.load(file_name)




if __name__ == "__main__":
    main()