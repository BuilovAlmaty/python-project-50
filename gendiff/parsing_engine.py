from functools import reduce

INDENT_COUNT = 4


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
        lambda acc, t: acc + f"    {t[0]} {t[1]}: {t[2]}\n",
        generate_diff_between_dicts(dict1, dict2), ""
    )
    return total.rstrip()


def get_list_compare_two_dicts(first_dict, second_dict=None, space=0):
    space += INDENT_COUNT
    output = []

    if second_dict is None:
        for k, v in first_dict.items():
            if isinstance(v, dict):
                output.append((k, "parent", space, " "))
                output.extend(get_list_compare_two_dicts(v, space=space))
            else:
                output.append((k, v, space, " "))
        return output

    keys = sorted(first_dict.keys() | second_dict.keys())
    for k in keys:
        if k in first_dict and k in second_dict:
            if isinstance(first_dict[k], dict) and isinstance(second_dict[k], dict):
                output.append((k, "parent", space, " "))
                output.extend(get_list_compare_two_dicts(first_dict[k], second_dict[k], space))
            elif isinstance(first_dict[k], dict):
                output.append((k, "parent", space, "-"))
                output.extend(get_list_compare_two_dicts(first_dict[k], space=space))
                output.append((k, second_dict[k], space, "+"))
            elif isinstance(second_dict[k], dict):
                output.extend(get_list_compare_two_dicts(second_dict[k], space=space))
                output.append((k, first_dict[k], space, "+"))
            else:
                if first_dict[k] == second_dict[k]:
                    output.append((k, first_dict[k], space, " "))
                else:
                    output.append((k, first_dict[k], space, "-"))
                    output.append((k, second_dict[k], space, "+"))
        elif k in first_dict:
            if isinstance(first_dict[k], dict):
                output.append((k, "parent", space, "-"))
                output.extend(get_list_compare_two_dicts(first_dict[k], space=space))
            else:
                output.append((k, first_dict[k], space, "-"))
        elif k in second_dict:
            if isinstance(second_dict[k], dict):
                output.append((k, "parent", space, "+"))
                output.extend(get_list_compare_two_dicts(second_dict[k], space=space))
            else:
                output.append((k, second_dict[k], space, "+"))
    return output


def formatter(tree_as_list):
    space_sign = " "
    output_text = ""
    stack = []
    for i in tree_as_list:

        # output "}" sign
        while stack and i[2] <= stack[-1]:
           output_text += f"{space_sign * (stack.pop() + 2)}}}\n"

        if i[1] == "parent":
            output_text += f"{space_sign * i[2]}{i[3]} {i[0]}: {{\n"
            stack.append(i[2])
        else:
            value = str(i[1])
            if isinstance(i[1], bool):
                value = value.lower()
            if i[1] is None:
                value = "null"
            output_text += f"{space_sign * i[2]}{i[3]} {i[0]}: {value}\n"

    while stack:
        output_text += f"{space_sign * (stack.pop() + 2)}}}\n"

    return output_text.rstrip()


def generate_diff(dict1, dict2, format_name='stylish'):
    value = ""
    if format_name == "stylish":
        diff = get_list_compare_two_dicts(dict1, dict2)
        value = formatter(diff)
    elif format_name == "linear":
        value = generate_linear_diff(dict1, dict2)

    if value:
        value = f"{{\n{value}\n}}"

    return value
