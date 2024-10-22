from helper.header_helper import HeaderInit


class OpenTixHeader(HeaderInit):
    def get_header(self) -> dict[str, str] | None:
        return {
            "User-Agent": self.get_random_user_agent(),
            "origin": "https://www.opentix.life",
            "referer": "https://www.opentix.life/",
        }
