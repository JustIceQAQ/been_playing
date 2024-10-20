from helper.header_helper import HeaderInit


class TFAMLifeHeader(HeaderInit):
    def get_header(self) -> dict[str, str]:
        return {
            "user-agent": self.get_random_user_agent(),
            "Referer": "https://www.tfam.museum/Exhibition/Exhibition.aspx?ddlLang=zh-tw",
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "www.tfam.museum",
            "X-Requested-With": "XMLHttpRequest",
        }
