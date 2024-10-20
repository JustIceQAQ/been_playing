from helper.header_helper import HeaderInit


class IBonHeader(HeaderInit):
    def get_header(self) -> dict[str, str] | None:
        return {
            "User-Agent": self.get_random_user_agent(),
            "Referer": "https://tour.ibon.com.tw/home/search?category=exhibition",
        }
