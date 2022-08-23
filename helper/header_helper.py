from abc import ABCMeta, abstractmethod
from typing import Dict, Optional

USER_AGENT = (
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/102.0.5005.61 "
    "Safari/537.36"
)


class HeaderInit(metaclass=ABCMeta):
    @abstractmethod
    def get_header(self) -> Optional[Dict[str, str]]:
        raise NotImplementedError


class TicketsUdnFunLifeHeader(HeaderInit):
    def get_header(self) -> Dict[str, str]:
        return {
            "User-Agent": USER_AGENT,
            "Host": "tickets.udnfunlife.com",
            "Origin": "https://tickets.udnfunlife.com",
            "Referer": "https://tickets.udnfunlife.com/application/UTK01/UTK0101_.aspx",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        }


class TFAMLifeHeader(HeaderInit):
    def get_header(self) -> Dict[str, str]:
        return {
            "user-agent": USER_AGENT,
            "Referer": "https://www.tfam.museum/Exhibition/Exhibition.aspx?ddlLang=zh-tw",
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "www.tfam.museum",
            "X-Requested-With": "XMLHttpRequest",
        }


class TicketsBooksHeader(HeaderInit):
    def get_header(self) -> Dict[str, str]:
        return {
            "User-Agent": USER_AGENT,
            "Host": "tickets.books.com.tw",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }


class NMHHeader(HeaderInit):
    def get_header(self) -> Dict[str, str]:
        return {
            "User-Agent": USER_AGENT,
            "Host": "www.nmh.gov.tw",
            "Referer": "https://www.nmh.gov.tw/activitysoonlist_66.html",
        }


class TWTCHeader(HeaderInit):
    def get_header(self) -> Dict[str, str]:
        return {
            "User-Agent": USER_AGENT,
            "Host": "twtc.com.tw",
            "Pragma": "no-cache",
        }
