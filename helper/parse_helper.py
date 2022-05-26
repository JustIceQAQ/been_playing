import inspect
from abc import ABCMeta, abstractmethod

import bs4
import cssutils


class ParseInit(metaclass=ABCMeta):
    @abstractmethod
    def get_title(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_date(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_address(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_figure(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_source_url(self, *args, **kwargs):
        raise NotImplementedError

    def parsed(self, *args, **kwargs):
        methods = [
            method
            for method in inspect.getmembers(self, predicate=inspect.ismethod)
            if method[0].startswith("get_")
        ]
        return {
            def_name.split("get_")[-1]: method(*args, **kwargs)
            for def_name, method in methods
        }


class MocaTaipeiParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("h3", {"class": "imgTitle"}).get_text()

    def get_date(self, *args, **kwargs):
        return self.item.find("div", {"class": "dateBox"}).get_text()

    def get_address(self, *args, **kwargs):
        return "-"

    def get_figure(self, *args, **kwargs):
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(
            target_domain, self.item.select_one("figure.imgFrame img")["data-src"]
        )

    def get_source_url(self, *args, **kwargs):
        return self.item.select_one("a.textFrame")["href"]


class NpmRowParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("h3", {"class": "font-medium"}).get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.find("div", {"class": "exhibition-list-date"}).get_text()

    def get_address(self, *args, **kwargs) -> str:
        return self.item.find("div", {"class": "card-content-bottom"}).get_text()

    def get_figure(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(
            target_domain, self.item.select_one("figure.card-image img")["data-src"]
        )

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")

        used_this_to_clean = kwargs.get("used_this_to_clean", None)
        if used_this_to_clean is None:
            return "{}{}".format(target_domain, self.item.select_one("a.card")["href"])
        else:
            return "{}{}".format(
                target_domain,
                used_this_to_clean(self.item.select_one("a.card")["href"]),
            )


class NpmColParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("h3", {"class": "card-title-underline"}).get_text()

    def get_date(self, *args, **kwargs) -> str:
        return "-"

    def get_address(self, *args, **kwargs) -> str:
        return self.item.find("div", {"class": "card-content-bottom"}).get_text()

    def get_figure(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(
            target_domain, self.item.select_one("figure.card-image img")["data-src"]
        )

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")

        used_this_to_clean = kwargs.get("used_this_to_clean", None)
        if used_this_to_clean is None:
            return "{}{}".format(target_domain, self.item.select_one("a.card")["href"])
        else:
            return "{}{}".format(
                target_domain,
                used_this_to_clean(self.item.select_one("a.card")["href"]),
            )


class CKSMHParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one("dt > a > div.h3").get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.select_one("dd > span.date").get_text()

    def get_address(self, *args, **kwargs) -> str:
        return self.item.select_one("dd > span.location").get_text()

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.select_one("dt > a > span > img")["src"]

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.select_one("dt > a")["href"]


class HuaShan1914Parse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one(
            "li > a > div > div > div.card-text > div.card-text-name"
        ).get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.select_one(
            "li > a > div > div > div.card-text > div.event-date"
        ).get_text()

    def get_address(self, *args, **kwargs) -> str:
        return "-"

    def get_figure(self, *args, **kwargs) -> str:
        # event-ul > li:nth-child(1) > a > div > div > div.card-img.wide
        dev_style = self.item.select_one("li > a > div > div > div.card-img.wide")[
            "style"
        ]
        style = cssutils.parseStyle(dev_style)

        return (
            url.replace("url(", "")[:-1].replace('"', "")
            if (url := style["background-image"])
            else "-"
        )

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(target_domain, self.item.select_one("li > a")["href"])


class SongShanCulturalParkParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs):
        return self.item.select_one("span.row_rt > p.lv_h2").get_text()

    def get_date(self, *args, **kwargs):
        return self.item.select_one("span.row_rt > p.date.montsrt").get_text()

    def get_address(self, *args, **kwargs):
        return ""

    def get_figure(self, *args, **kwargs):
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(
            target_domain, self.item.select_one("span.row_lt > img")["src"]
        )

    def get_source_url(self, *args, **kwargs):
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(
            target_domain, self.item.select_one("span.row_rt > a")["href"]
        )
