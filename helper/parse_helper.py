import datetime
import inspect
import json
import re
from abc import ABCMeta, abstractmethod
from typing import Any, AnyStr, Dict, List
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import bs4
import cssutils


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


class MocaTaipeiParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("h3", {"class": "imgTitle"}).get_text()

    def get_date(self, *args, **kwargs) -> str:
        raw_string = self.item.find("div", {"class": "dateBox"}).get_text()
        regulated = re.findall(
            r"(?P<year>\d{4})\s*(?P<month>\d{2})\s\/\s(?P<day>\d{2})", raw_string
        )
        start_date_regulated, end_date_regulated = regulated
        start_date = datetime.date(
            int(start_date_regulated[0]),
            int(start_date_regulated[1]),
            int(start_date_regulated[2]),
        ).isoformat()
        end_date = datetime.date(
            int(end_date_regulated[0]),
            int(end_date_regulated[1]),
            int(end_date_regulated[2]),
        ).isoformat()

        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str:
        return "-"

    def get_figure(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(
            target_domain, self.item.select_one("figure.imgFrame img")["data-src"]
        )

    def get_source_url(self, *args, **kwargs) -> str:
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

        figure_url = "{}{}".format(
            target_domain, self.item.select_one("figure.card-image img")["data-src"]
        )

        return self.clean_figure_url(figure_url)

    def clean_figure_url(self, o_url):
        u = urlparse(o_url)
        query = parse_qs(u.query, keep_blank_values=True)
        for word in {"w", "h"}:
            query.pop(word, None)
        u = u._replace(query=urlencode(query, True))
        return urlunparse(u)

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
        return self.item.select_one("dd > span.date").get_text().replace("/", "-")

    def get_address(self, *args, **kwargs) -> str:
        return self.item.select_one("dd > span.location").get_text()

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.select_one("dt > a > span > img")["src"]

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.select_one("dt > a")["href"]


class HuaShan1914Parse(ParseInit):
    def __init__(self, item: bs4.element.Tag) -> None:
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one(
            "li > a > div > div > div.card-text > div.card-text-name"
        ).get_text()

    def get_date(self, *args, **kwargs) -> str:
        raw_string = self.item.select_one(
            "li > a > div > div > div.card-text > div.event-date"
        ).get_text()
        if "-" in raw_string:
            row_start_date, row_end_date = raw_string.split(" - ")
            regulated_start_date = re.search(
                r"((?P<year>\d{4})\.(?P<month>\d{2})\.(?P<day>\d{2}))", row_start_date
            )
            start_date = datetime.date(
                int(regulated_start_date.group("year")),
                int(regulated_start_date.group("month")),
                int(regulated_start_date.group("day")),
            )
            regulated_end_date = re.search(
                r"((?P<year>\d{4})?\.?(?P<month>\d{2})\.(?P<day>\d{2}))", row_end_date
            )
            end_date = datetime.date(
                int(
                    year
                    if (year := regulated_end_date.group("year"))
                    else start_date.year
                ),
                int(regulated_end_date.group("month")),
                int(regulated_end_date.group("day")),
            )

            cooked_string = f"{start_date.isoformat()} ~ {end_date.isoformat()}"
        else:
            # one day case
            regulated = re.search(
                r"((?P<year>\d{4})\.(?P<month>\d{2})\.(?P<day>\d{2}))", raw_string
            )
            start_date = datetime.date(
                int(regulated.group("year")),
                int(regulated.group("month")),
                int(regulated.group("day")),
            ).isoformat()
            end_date = start_date
            cooked_string = f"{start_date} ~ {end_date}"
        return cooked_string

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

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one("span.row_rt > p.lv_h2").get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.select_one("span.row_rt > p.date.montsrt").get_text()

    def get_address(self, *args, **kwargs) -> str:
        return "-"

    def get_figure(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(
            target_domain, self.item.select_one("span.row_lt > img")["src"]
        )

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(
            target_domain, self.item.select_one("span.row_rt > a")["href"]
        )


class NTSECParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one("div.message > h3").get_text()

    def get_date(self, *args, **kwargs) -> str:
        return "-"

    def get_address(self, *args, **kwargs) -> str:
        return "-"

    def get_figure(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(
            target_domain,
            self.item.select_one("div.photo > img")["src"].replace("../", "/"),
        )

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}/User/{}".format(
            target_domain, self.item.select_one("li > a")["href"]
        )


class TFAMParse(ParseInit):
    def __init__(self, item: Dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return str(self.item.get("ExName", "-"))

    def get_date(self, *args, **kwargs) -> str:
        begin_date = self.item.get("BeginDate", None)
        end_date = self.item.get("EndDate", None)
        return f"{begin_date} ~ {end_date}".replace("/", "-")

    def get_address(self, *args, **kwargs) -> str:
        return self.item.get("Area", "-")

    def get_figure(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        now_play_img = self.item.get("NowPlayImg", None)

        return "{}/File/{}".format(target_domain, now_play_img.replace("\\", "/"))

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")

        return "{}/Exhibition/Exhibition_page.aspx?id={}".format(
            target_domain, self.item.get("ExID", "-")
        )


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


class NTMParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one("dd > h2 > a").get_text()

    def get_date(self, *args, **kwargs) -> str:
        return "".join(
            [
                label.get_text().strip()
                for label in self.item.select("dd > ul > li:nth-child(1) > label")
            ]
        ).replace("/", "-")

    def get_address(self, *args, **kwargs) -> str:
        return self.item.select_one("dd > ul > li:nth-child(2)").get_text()

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.select_one("dt > a")["href"]

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.select_one("dd > h2 > a")["href"]


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


class NMHParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("p", {"class": "tit"}).get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.find("p", {"class": "time"}).get_text()

    def get_address(self, *args, **kwargs) -> str:
        return self.item.find("p", {"class": "address"}).get_text()

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.find("img").get("src", None)

    def get_source_url(self, *args, **kwargs) -> str:
        return self.item.find("a").get("href", None)


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


class MWRParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.select_one("div.title > a").get_text()

    def get_date(self, *args, **kwargs) -> str:
        return self.item.select_one("div.date").get_text()

    def get_address(self, *args, **kwargs) -> str:
        return "-"

    def get_figure(self, *args, **kwargs) -> str:
        dev_style = self.item.select_one("div.imgBox > a > div.img").get("style")
        style = cssutils.parseStyle(dev_style)

        return (
            url.replace("url(", "")[:-1].replace('"', "")
            if (url := style["background-image"])
            else "-"
        )

    def get_source_url(self, *args, **kwargs) -> str:
        pre_path = "https://www.mwr.org.tw/{}"
        return pre_path.format(self.item.select_one("div.title > a").get("href"))


class MuseumPostParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.find("h3").get_text()

    def get_date(self, *args, **kwargs) -> str:
        date_value = "-"
        if runtime_value := self.item.find("div", {"class": "ex_date"}):
            date_value = runtime_value.get_text().replace("日期：", "").strip()
        return date_value

    def get_address(self, *args, **kwargs) -> str:
        address_value = "-"
        if runtime_value := self.item.find("div", {"class": "ex_place"}):
            address_value = runtime_value.get_text().replace("地點：", "").strip()
        return address_value

    def get_figure(self, *args, **kwargs) -> str:
        return self.item.find("img").get("src")

    def get_source_url(self, *args, **kwargs) -> str:
        pre_url = "https://museum.post.gov.tw/post/Postal_Museum/museum/{}"
        return pre_url.format(
            self.item.find("div", {"class": "textWrap"}).find("a").get("href")
        )
