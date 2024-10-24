from abc import ABCMeta


class CleanInit(metaclass=ABCMeta):
    @staticmethod
    def clean_string(raw_string) -> str:
        raise NotImplementedError


class RequestsClean(CleanInit):
    @staticmethod
    def clean_string(raw_string: str) -> str:
        # TODO: big5 utf-8
        if raw_string is None:
            return None
        replace_string_set = {"日期：", " more", "地點："}
        for replace_string in replace_string_set:
            raw_string = raw_string.replace(replace_string, " ")
        return " ".join(raw_string.split()).strip()
