import random
import secrets
from abc import ABCMeta, abstractmethod
from typing import Dict, Optional

USER_AGENT = (
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/102.0.5005.61 "
    "Safari/537.36"
)
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
]


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


class MWRHeader(HeaderInit):
    def get_header(self) -> Dict[str, str]:
        return {
            "User-Agent": USER_AGENT,
            "referer": "https://www.mwr.org.tw/xcpmtexhi?xsmsid=0H305740978429024070",
        }


class MuseumPostHeader(HeaderInit):
    def get_header(self) -> Optional[Dict[str, str]]:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "Host": "museum.post.gov.tw",
            "Referer": "https://museum.post.gov.tw/post/Postal_Museum/museum/",
            "Cookie": f"JSESSIONID={secrets.token_hex(16).upper()}; fwchk={secrets.token_hex(15)}+",
            "Connection": "close",
        }


class JamHeader(HeaderInit):
    def get_header(self) -> Optional[Dict[str, str]]:
        return {
            "User-Agent": random.choice(USER_AGENT_LIST),
            "Host": "jam.jutfoundation.org.tw",
            "Referer": "http://jam.jutfoundation.org.tw",
        }
