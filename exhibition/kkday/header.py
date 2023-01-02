import random
from typing import Dict, Optional

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class KKDayHeader(HeaderInit):
    def get_header(self) -> Optional[Dict[str, str]]:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "host": "www.kkday.com",
            "Referer": "https://www.kkday.com/zh-tw/country/taiwan/events-and-exhibitions?cat=TAG_3&sort=prec&page=1",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }