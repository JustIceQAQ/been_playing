import random
import secrets

from helper.header_helper import USER_AGENT_LIST, HeaderInit


class NCPIHeader(HeaderInit):
    def get_header(self) -> dict[str, str] | None:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "Host": "ncpi.ntmofa.gov.tw",
            "Cookie": f"ASP.NET_SessionId={secrets.token_hex(12)}",
        }


class NCPIVisitHeader(HeaderInit):
    def get_header(self) -> dict[str, str] | None:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "Host": "ncpi.ntmofa.gov.tw",
            "Cookie": f"ASP.NET_SessionId={secrets.token_hex(12).lower()};",
        }
