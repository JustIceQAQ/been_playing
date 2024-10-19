import random

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class CLabHeader(HeaderInit):
    def get_header(self) -> dict[str, str]:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
        }
