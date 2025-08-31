import argparse
import json
from functools import reduce

__version__ = "0.1.1"


def generate_diff(dict1, dict2):

    total = reduce(
        lambda acc, t: acc + f"{t[0]} {t[1]}: {t[2]}\n",
        generate_diff_between_dicts(dict1, dict2), ""
    )
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

    try:
        with open(args.first_file, encoding="utf-8") as f:
            dict1 = json.load(f)
        with open(args.second_file, encoding="utf-8") as f:
            dict2 = json.load(f)
    except json.JSONDecodeError as e:
        print(f'Json file read error: {e}')
        return

    diff = generate_diff(dict1, dict2)

    if diff:
        print(f"{{\n{diff}\n}}")


if __name__ == "__main__":
    main()
