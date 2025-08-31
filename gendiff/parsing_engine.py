from functools import reduce


def generate_linear_diff(dict1, dict2):
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

    total = reduce(
        lambda acc, t: acc + f"{t[0]} {t[1]}: {t[2]}\n",
        generate_diff_between_dicts(dict1, dict2), ""
    )
    return total.rstrip()
