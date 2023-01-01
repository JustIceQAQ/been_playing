import random
from typing import Dict

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class TFAMLifeHeader(HeaderInit):
    def get_header(self) -> Dict[str, str]:
        return {
            "user-agent": random.choice(USER_AGENT_LIST),
            "Referer": "https://www.tfam.museum/Exhibition/Exhibition.aspx?ddlLang=zh-tw",
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "www.tfam.museum",
            "X-Requested-With": "XMLHttpRequest",
        }
