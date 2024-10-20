from helper.header_helper import HeaderInit


class CLabHeader(HeaderInit):
    def get_header(self) -> dict[str, str]:
        return {
            "User-Agent": self.get_random_user_agent(),
        }
