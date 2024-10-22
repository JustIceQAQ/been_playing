from helper.header_helper import HeaderInit


class TicketsUdnFunLifeHeader(HeaderInit):
    def get_header(self) -> dict[str, str]:
        return {
            "User-Agent": self.get_random_user_agent(),
            "Host": "tickets.udnfunlife.com",
            "Origin": "https://tickets.udnfunlife.com",
            "Referer": "https://tickets.udnfunlife.com/application/UTK01/UTK0101_.aspx",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        }


class TicketsUdnFunLifeCookieHeader(HeaderInit):
    def get_header(self) -> dict[str, str]:
        return {
            "User-Agent": self.get_random_user_agent(),
            "Host": "tickets.udnfunlife.com",
            "upgrade-insecure-requests": "1",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
        }
