from functools import reduce


def generate_linear_diff(dict1, dict2):
    def generate_diff_between_dicts(dict1, dict2):
        keys = sorted(set(dict1.keys() | dict2.keys()))
        for k in keys:
            if k in dict1 and k in dict2:
                if dict1[k] == dict2[k]:
                    yield (' ', k, format_value(dict1[k]))
                else:
                    yield ('-', k, format_value(dict1[k]))
                    yield ('+', k, format_value(dict2[k]))
            elif k in dict2:
                yield ('+', k, format_value(dict2[k]))
            else:
                yield ('-', k, format_value(dict1[k]))

    def format_value(value):
        output_value = str(value)
        if isinstance(value, bool):
            output_value = output_value.lower()
        if value is None:
            output_value = "null"
        return output_value

    total = reduce(
        lambda acc, t: acc + f"  {t[0]} {t[1]}: {t[2]}\n",
        generate_diff_between_dicts(dict1, dict2), ""
    )
    return f"{{\n{total.rstrip()}\n}}"
