def plain(diff):
    def _plain_formatter(diff, parent_name=""):
        lines = []
        for node in diff:
            key = node["key"]
            status = node["status"]
            full_name = "Property \'" + f"{parent_name}.{key}\'"[1:]
            if status == "nested":
                lines.extend(_plain_formatter(node["children"], f"{parent_name}.{key}"))
            elif status == "added":
                value = _format_value(node['value'])
                line = f"{full_name} was added with value: {value}"
                lines.append(line)
            elif status == "updated":
                new_value = _format_value(node['new_value'])
                old_value = _format_value(node['old_value'])
                line = f"{full_name} was updated. From {old_value} to {new_value}"
                lines.append(line)
            elif status == "removed":
                line = f"{full_name} was removed"
                lines.append(line)

        return lines
    return "\n".join(_plain_formatter(diff))


def _format_value(value):
    if isinstance(value, dict):
        return "[complex value]"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    return f"\'{value}\'"
