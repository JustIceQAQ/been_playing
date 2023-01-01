import random
from typing import Dict

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class MWRHeader(HeaderInit):
    def get_header(self) -> Dict[str, str]:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "referer": "https://www.mwr.org.tw/xcpmtexhi?xsmsid=0H305740978429024070",
        }
