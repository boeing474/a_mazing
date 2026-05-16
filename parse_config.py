import sys
import os

def parse_to_dict(raw_content: str) -> dict[str, str]:
    """Parses text content into a configuration dictionary."""
    content_dict: dict[str, str] = {}
    lines = raw_content.split("\n")
    
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        
        if not line or line.startswith("#"):
            continue
        
        if "=" not in line:
            print(f"Error: Invalid format on line {line_num}: '{line}' (Missing '=')")
            sys.exit(1)
            
        key, value = line.split("=", 1)
        content_dict[key.strip()] = value.strip()
        
    return content_dict

def validate_keys(parsed_config: dict[str, str]) -> None:
    """Checks if all required keys are present."""
    required_keys = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}
    missing_keys = required_keys - parsed_config.keys()
    
    if missing_keys:
        print(f"Error: Missing required configuration keys: {', '.join(missing_keys)}")
        sys.exit(1)

def load(file_path: str) -> dict[str, str]:
    """Reads the file and returns the validated configuration dictionary."""
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
        
    try:
        with open(file_path, "r") as f:
            raw_content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    parsed_config = parse_to_dict(raw_content)
    validate_keys(parsed_config)
    
    return parsed_config

def main() -> None:
    pass

if __name__ == "__main__":
    main()
