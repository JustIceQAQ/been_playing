from helper.header_helper import HeaderInit


class NTSECHeader(HeaderInit):
    def get_header(self) -> dict[str, str] | None:
        return {
            "User-Agent": self.get_random_user_agent(),
            "Host": "www.ntsec.gov.tw",
        }
