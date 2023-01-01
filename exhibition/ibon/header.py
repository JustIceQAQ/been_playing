import random
from typing import Dict, Optional

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class IBonHeader(HeaderInit):
    def get_header(self) -> Optional[Dict[str, str]]:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "Referer": "https://tour.ibon.com.tw/home/search?category=exhibition",
        }
