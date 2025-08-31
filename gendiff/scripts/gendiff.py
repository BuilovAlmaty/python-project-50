import argparse
import json
from pathlib import Path

import yaml

from gendiff.parsing_engine import generate_linear_diff

__version__ = "0.1.2"


def load_file(path):
    path = Path(path)
    try:
        with open(path, encoding="utf-8") as f:
            if path.suffix == ".json":
                return json.load(f)
            elif path.suffix in (".yaml", ".yml"):
                return yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported file format: {path.suffix}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON file read error ({path}): {e}")
    except yaml.YAMLError as e:
        raise ValueError(f"YAML file read error ({path}): {e}")


def load_files(first_path, second_path):
    dict1 = load_file(first_path)
    dict2 = load_file(second_path)
    return dict1, dict2


def main():
    parser = argparse.ArgumentParser(
        prog="gendiff",
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("first_file", help="Path to the first file")
    parser.add_argument("second_file", help="Path to the second file")
    parser.add_argument(
        "-f", "--format",
        default="plain",
        choices=[
            "plain",
            "json",
            "yml",
            "yaml"
        ],
        help="Set format of output (default: plain)"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    dict1, dict2 = load_files(args.first_file, args.second_file)
    diff = generate_linear_diff(dict1, dict2)

    if diff:
        print(f"{{\n{diff}\n}}")


if __name__ == "__main__":
    main()
