import random
import secrets
from typing import Dict, Optional

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class NCPIHeader(HeaderInit):
    def get_header(self) -> Optional[Dict[str, str]]:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "Host": "ncpiexhibition.ntmofa.gov.tw",
            "Cookie": "Localization.CurrentUICulture=tw",
        }


class NCPIVisitHeader(HeaderInit):
    def get_header(self) -> Optional[Dict[str, str]]:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "Host": "ncpi.ntmofa.gov.tw",
            "Cookie": f"ASP.NET_SessionId={secrets.token_hex(12).lower()};",
        }
