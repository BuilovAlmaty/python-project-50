def stylish(diff):
    def _stylish_formatter(_diff, depth=0):
        lines = []
        indent = " " * (depth * 4)

        for node in _diff:
            key = node["key"]
            status = node["status"]

            if status == "nested":
                children = _stylish_formatter(node["children"], depth + 1)
                lines.append(f"{indent}    {key}: {{\n{children}\n{indent}    }}")

            elif status == "unchanged":
                val = _format_value(node["value"], depth + 1)
                lines.append(f"{indent}    {key}: {val}")

            elif status == "removed":
                val = _format_value(node["value"], depth + 1)
                lines.append(f"{indent}  - {key}: {val}")

            elif status == "added":
                val = _format_value(node["value"], depth + 1)
                lines.append(f"{indent}  + {key}: {val}")

            elif status == "updated":
                old_val = _format_value(node["old_value"], depth + 1)
                new_val = _format_value(node["new_value"], depth + 1)
                lines.append(f"{indent}  - {key}: {old_val}")
                lines.append(f"{indent}  + {key}: {new_val}")

        return "\n".join(lines)
    return "{\n" + _stylish_formatter(diff) + "\n}"


def _format_value(value, depth):
    indent = " " * (depth * 4)
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            lines.append(f"{indent}    {k}: {_format_value(v, depth + 1)}")
        return "{\n" + "\n".join(lines) + f"\n{indent}}}"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    return str(value)
