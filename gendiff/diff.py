def get_diff(dict1, dict2):
    keys = sorted(dict1.keys() | dict2.keys())
    diff = []
    for k in keys:
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                diff.append({
                    "key": k,
                    "status": "nested",
                    "children": get_diff(dict1[k], dict2[k])
                })
            elif dict1[k] == dict2[k]:
                diff.append({"key": k, "status": "unchanged", "value": dict1[k]})
            else:
                diff.append({"key": k, "status": "updated", "old_value": dict1[k], "new_value": dict2[k]})
        elif k in dict1:
            diff.append({"key": k, "status": "removed", "value": dict1[k]})
        else:
            diff.append({"key": k, "status": "added", "value": dict2[k]})
    return diff















