import secrets

from helper.header_helper import HeaderInit


class NCPIHeader(HeaderInit):
    def get_header(self) -> dict[str, str] | None:
        return {
            "User-Agent": self.get_random_user_agent(),
            "Host": "ncpi.ntmofa.gov.tw",
            "Cookie": f"ASP.NET_SessionId={secrets.token_hex(12)}",
        }


class NCPIVisitHeader(HeaderInit):
    def get_header(self) -> dict[str, str] | None:
        return {
            "User-Agent": self.get_random_user_agent(),
            "Host": "ncpi.ntmofa.gov.tw",
            "Cookie": f"ASP.NET_SessionId={secrets.token_hex(12).lower()};",
        }
