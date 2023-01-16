import random
from typing import Dict, Optional

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class NTSECHeader(HeaderInit):
    def get_header(self) -> Optional[Dict[str, str]]:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "Host": "www.ntsec.gov.tw",
        }