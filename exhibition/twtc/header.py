from helper.header_helper import HeaderInit


class TWTCHeader(HeaderInit):
    def get_header(self) -> dict[str, str]:
        return {
            "User-Agent": self.get_random_user_agent(),
            "Host": "twtc.com.tw",
            "Pragma": "no-cache",
            "Referer": "https://twtc.com.tw/exhibition?p=home",
        }
