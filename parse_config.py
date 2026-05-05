def parse_to_dict(raw_content: str) -> dict:
    content_dict = dict(item.split("=") for item in raw_content.split("\n"))
    return content_dict


def load(file: str) -> None:
    try:
        with open(file, "r") as f:
            raw_content = f.read()
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)

    configs = parse_to_dict(raw_content)


def main():
    pass


if __name__ == "__main__":
    main()

# teste main
# teste ramon