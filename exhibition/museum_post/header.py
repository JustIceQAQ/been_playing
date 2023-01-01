import random
import secrets
from typing import Dict, Optional

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class MuseumPostHeader(HeaderInit):
    def get_header(self) -> Optional[Dict[str, str]]:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "Host": "museum.post.gov.tw",
            "Referer": "https://museum.post.gov.tw/post/Postal_Museum/museum/",
            "Cookie": f"JSESSIONID={secrets.token_hex(16).upper()}; fwchk={secrets.token_hex(15)}+",
            "Connection": "close",
        }
