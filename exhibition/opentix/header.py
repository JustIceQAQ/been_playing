import random

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class OpenTixHeader(HeaderInit):
    def get_header(self) -> dict[str, str] | None:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "origin": "https://www.opentix.life",
            "referer": "https://www.opentix.life/",
        }
