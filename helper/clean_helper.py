from abc import ABCMeta


class CleanInit(metaclass=ABCMeta):
    @staticmethod
    def clean_string(raw_string):
        raise NotImplementedError


class RequestsClean(CleanInit):
    @staticmethod
    def clean_string(raw_string: str) -> str:
        replace_string_set = {"\u3000", "\n"}
        for replace_string in replace_string_set:
            raw_string = raw_string.replace(replace_string, " ")
        return ' '.join(raw_string.split()).strip()
