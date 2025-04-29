import json
import pathlib


class SuffixHelper:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        root_path = pathlib.Path(__file__).parent.parent.absolute()
        with open(
            root_path / pathlib.Path("fixture") / pathlib.Path("suffix_file.json"),
            "r",
            encoding="utf-8",
        ) as f:
            self.suffixes = json.load(f)

    def get_code_name_items(self, code_name: str) -> dict:
        return self.suffixes[code_name]


suffix_helper = SuffixHelper()
