import random

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class FuBonArtMuseumHeader(HeaderInit):
    def get_header(self) -> dict[str, str] | None:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
        }
