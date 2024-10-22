from helper.header_helper import HeaderInit


class TMCHeader(HeaderInit):
    def get_header(self) -> dict[str, str]:
        return {
            "accept": "text/html,"
            "application/xhtml+xml,"
            "application/xml;q=0.9,"
            "image/avif,"
            "image/webp,"
            "image/apng,*/*;q=0.8,"
            "application/signed-exchange;v=b3;q=0.7",
            "User-Agent": self.get_random_user_agent(),
            "Host": "www.tmc.taipei",
        }
