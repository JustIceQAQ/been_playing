import random

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class TWTCHeader(HeaderInit):
    def get_header(self) -> dict[str, str]:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "Host": "twtc.com.tw",
            "Pragma": "no-cache",
            "Referer": "https://twtc.com.tw/exhibition?p=home",
        }
