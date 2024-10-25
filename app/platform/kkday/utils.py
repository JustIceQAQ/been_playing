def parse_list(data: dict) -> dict:
    result = {}
    for key, value in data.items():
        if isinstance(value, list):
            result[key] = ",".join(value)
        else:
            result[key] = value
    return result
