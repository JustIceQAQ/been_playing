from helper.header_helper import HeaderInit


class MWRHeader(HeaderInit):
    def get_header(self) -> dict[str, str]:
        return {
            "User-Agent": self.get_random_user_agent(),
            "referer": "https://www.mwr.org.tw/xcpmtexhi?xsmsid=0H305740978429024070",
        }
