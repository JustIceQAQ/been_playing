import random
from typing import Dict

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class TMCHeader(HeaderInit):
    def get_header(self) -> Dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "User-Agent": random.choice(USER_AGENT_LIST),
            "Host": "www.tmc.taipei",
        }
