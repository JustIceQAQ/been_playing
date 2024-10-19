import random

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class NTSECHeader(HeaderInit):
    def get_header(self) -> dict[str, str] | None:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "Host": "www.ntsec.gov.tw",
        }
