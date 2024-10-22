from helper.header_helper import HeaderInit


class JamHeader(HeaderInit):
    def get_header(self) -> dict[str, str] | None:
        return {
            "User-Agent": self.get_random_user_agent(),
            "Host": "jam.jutfoundation.org.tw",
            "Referer": "http://jam.jutfoundation.org.tw",
        }
