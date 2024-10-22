import secrets

from helper.header_helper import HeaderInit


class MuseumPostHeader(HeaderInit):
    def get_header(self) -> dict[str, str] | None:
        return {
            "User-Agent": self.get_random_user_agent(),
            "Host": "museum.post.gov.tw",
            "Referer": "https://museum.post.gov.tw/post/Postal_Museum/museum/",
            "Cookie": f"JSESSIONID={secrets.token_hex(16).upper()}; fwchk={secrets.token_hex(15)}+",
            "Connection": "close",
        }
