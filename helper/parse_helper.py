import inspect
import json
from abc import ABCMeta, abstractmethod
from typing import Any, AnyStr, Dict, List
from urllib.parse import parse_qs, urlparse

import bs4


class ParseInit(metaclass=ABCMeta):
    @abstractmethod
    def get_title(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_date(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_address(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_figure(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_source_url(self, *args, **kwargs) -> str:
        raise NotImplementedError

    def parsed(self, *args, **kwargs) -> Dict[str, Any]:
        methods = [
            method
            for method in inspect.getmembers(self, predicate=inspect.ismethod)
            if method[0].startswith("get_")
        ]
        return {
            def_name.split("get_")[-1]: method(*args, **kwargs)
            for def_name, method in methods
        }


class TicketsUdnFunLifeParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("h5", {"class": "yd_card-title"}).get_text()

    def get_date(self, *args, **kwargs) -> str:
        icon_texts = self.item.findAll("div", {"class": "yd_card-iconText"})
        date_value = ""
        for icon_text in icon_texts:
            if "icon-date" in icon_text.find("img")["src"]:
                date_value = icon_text.find("div", {"class": "ellipsis"}).get_text()
                break
        return date_value

    def get_address(self, *args, **kwargs) -> str:
        icon_texts = self.item.findAll("div", {"class": "yd_card-iconText"})
        date_value = "-"
        for icon_text in icon_texts:
            if "icon-loc" in icon_text.find("img")["src"]:
                date_value = icon_text.find("div", {"class": "ellipsis"}).get_text()
                break
        return date_value

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.select_one("div.yd_card-thumbnail > img")["src"]

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.select_one("div.inner > a")["href"]


class TicketsBooksParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one("div.info > div > h4 > span > a").get_text()

    def get_date(self, *args, **kwargs) -> str:
        return "-"

    def get_address(self, *args, **kwargs) -> str:
        return "-"

    def get_figure(self, *args, **kwargs) -> str:
        return self.clean_figure_url(
            self.item.select_one("div.covbg > div > div > p > a > img")["src"]
        )

    def clean_figure_url(self, o_url) -> str:
        u = urlparse(o_url)
        query: Dict[AnyStr, List[AnyStr]] = parse_qs(u.query, keep_blank_values=True)
        runtime_url = o_url
        query_i: List[str] = query.get("i")
        if query_i and (get_url := query_i[0]):
            runtime_url = get_url
        return runtime_url

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.select_one("div.covbg > div > div > p > a")["href"]


class TMCParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("p", {"class": "m-event-card__box-title"}).get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.find(
            "p", {"class": "m-event-card__box-bottom-date"}
        ).get_text()

    def get_address(self, *args, **kwargs) -> str:
        return self.item.find(
            "p", {"class": "m-event-card__box-bottom-location"}
        ).get_text()

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.find("div", {"class": "m-event-card__img"})["data-bg"]

    def get_source_url(self, *args, **kwargs) -> str:
        o_archive_frame__item_wrap = self.item.find(
            "div", {"class": "o-archive-frame__item-wrap"}
        )
        if this_a := o_archive_frame__item_wrap.find("a", {"class": "m-event-card"}):
            return this_a.get("href", "")
        else:
            data_session = o_archive_frame__item_wrap["data-session"]
            data_session_json = json.loads(data_session)
            link = data_session_json[-1].get("link")
        return link


class TWTCParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item
        self.item_tds = item.select("td")

    def get_title(self, *args, **kwargs) -> str:
        return self.item_tds[1].get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item_tds[0].get_text()

    def get_address(self, *args, **kwargs) -> str:
        return self.item_tds[4].get_text()

    def get_figure(self, *args, **kwargs) -> str:
        return ""

    def get_source_url(self, *args, **kwargs) -> str:
        nth_child_a = self.item_tds[1].select("a")
        if len(nth_child_a) > 1:
            return nth_child_a[0].get("href", None)
        else:
            return "https://twtc.com.tw/" + nth_child_a[0].get("href", None)
