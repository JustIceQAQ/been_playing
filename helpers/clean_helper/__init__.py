from typing import Any

Values = str | list[Any] | None


class RequestsClean:
    @staticmethod
    def clean_string(raw_string: Values) -> Values:
        if raw_string is None:
            return None
        if isinstance(raw_string, list):
            return raw_string
        replace_string_set = {"日期：", " more", "地點："}
        for replace_string in replace_string_set:
            raw_string = raw_string.replace(replace_string, " ")
        return " ".join(raw_string.split()).strip()
