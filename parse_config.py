def load(file: str) -> None:
    try:
        with open(file, "r") as f:
            print(f.read())
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)

def main():
    pass

if __name__ == "__main__":
    main()