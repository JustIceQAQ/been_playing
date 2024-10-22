from helper.header_helper import HeaderInit


class NMHHeader(HeaderInit):
    def get_header(self) -> dict[str, str]:
        return {
            "User-Agent": self.get_random_user_agent(),
            "Host": "www.nmh.gov.tw",
            "Referer": "https://www.nmh.gov.tw/activitysoonlist_66.html",
        }
