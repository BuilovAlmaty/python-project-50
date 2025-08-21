import argparse
import json
from functools import reduce

__version__ = "0.1.1"

def generate_diff(file_path1, file_path2):
    with open(file_path1, encoding="utf-8") as f:
        dict1 = json.load(f)
    with open(file_path2, encoding="utf-8") as f:
        dict2 = json.load(f)

    total = reduce(lambda acc, t: acc + f"{t[0]} {t[1]}: {t[2]}\n", generate_diff_between_dicts(dict1, dict2), "")
    return total.rstrip()

def generate_diff_between_dicts(dict1, dict2):
    keys = sorted(set(dict1.keys() | dict2.keys()))

    for k in keys:
        if k in dict1 and k in dict2:
            if dict1[k] == dict2[k]:
                yield ('', k, dict1[k])
            else:
                yield ('-', k, dict1[k])
                yield ('+', k, dict2[k])
        elif k in dict2:
            yield ('+', k, dict2[k])
        else:
            yield ('-', k, dict1[k])

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
        choices=["plain", "json"],
        help="Set format of output (default: plain)"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    diff = generate_diff(args.first_file, args.second_file)

    print(f"{{\n{diff}\n}}")


if __name__ == "__main__":
    main()
