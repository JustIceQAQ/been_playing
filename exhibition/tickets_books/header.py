from helper.header_helper import HeaderInit


class TicketsBooksHeader(HeaderInit):
    def get_header(self) -> dict[str, str]:
        return {
            "User-Agent": self.get_random_user_agent(),
            "Host": "tickets.books.com.tw",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
