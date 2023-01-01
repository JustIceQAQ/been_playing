import random
from typing import Dict

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class NMHHeader(HeaderInit):
    def get_header(self) -> Dict[str, str]:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "Host": "www.nmh.gov.tw",
            "Referer": "https://www.nmh.gov.tw/activitysoonlist_66.html",
        }
