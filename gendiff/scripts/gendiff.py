import argparse
import json
from pathlib import Path

import yaml

from gendiff import get_diff
from gendiff.formatter import linear, plain, stylish

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
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found ({e.filename})")


def load_files(first_path, second_path):
    dict1 = load_file(first_path)
    dict2 = load_file(second_path)
    return dict1, dict2


def generate_diff(file_path1, file_path2, format_name="stylish"):
    dict1, dict2 = load_files(file_path1, file_path2)
    return generate_diff_dicts(dict1, dict2, format_name)


def generate_diff_dicts(dict1, dict2, format="stylish"):
    if format == "stylish":
        return stylish(get_diff(dict1, dict2))
    elif format == "linear":
        return linear(dict1, dict2)
    elif format == "plain":
        return plain(get_diff(dict1, dict2))
    elif format == "json":
        return json.dumps(get_diff(dict1, dict2))
    else:
        raise ValueError(f"Unknown format: {format}")


def main():
    parser = argparse.ArgumentParser(
        prog="gendiff",
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("first_file", help="Path to the first file")
    parser.add_argument("second_file", help="Path to the second file")
    parser.add_argument(
        "-f", "--format",
        default="stylish",
        choices=[
            "stylish",
            "linear",
            "plain",
            "json"
        ],
        help="Set format of output (default: stylish)"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    diff = generate_diff(args.first_file, args.second_file, args.format)

    if diff:
        print(diff)


if __name__ == "__main__":
    main()
