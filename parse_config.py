def load(file: str) -> None:
    try:
        with open(file, "r") as f:
            print(f.read())
    except Exception:
        pass

def main():
    pass

if __name__ == "__main__":
    main()