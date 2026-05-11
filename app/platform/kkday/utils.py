from collections.abc import Mapping


def parse_list(data: Mapping) -> dict:
    result = {}
    for key, value in data.items():
        if isinstance(value, list):
            result[key] = ",".join(value)
        else:
            result[key] = value
    return result
