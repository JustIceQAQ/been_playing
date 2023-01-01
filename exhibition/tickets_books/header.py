import random
from typing import Dict

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class TicketsBooksHeader(HeaderInit):
    def get_header(self) -> Dict[str, str]:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "Host": "tickets.books.com.tw",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }