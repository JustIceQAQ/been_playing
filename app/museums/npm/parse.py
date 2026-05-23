from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import bs4

from helpers.parse_helper import ParseInit
from helpers.utils_helper import to_ad_year


class NpmRowParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("h3", {"class": "font-medium"}).get_text()

    def get_date(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "exhibition-list-date"}).get_text().replace("~", " ~ ")

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "card-content-bottom"}).get_text()

    def get_figure(self, *args, **kwargs) -> str | None:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(target_domain, self.item.select_one("figure.card-image img")["data-src"])

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        tags = self.item.find("div", {"class": "exhibition-list-date"}).next_sibling.next_sibling
        if tags is None:
            return None
        tags = tags.get_text(strip=True)
        tags = [t.strip().replace("\u3000", "") for t in tags.split("#") if t.strip()]
        return tags

    def get_source_url(self, *args, **kwargs) -> str | None:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")

        return "{}{}".format(target_domain, self.item.select_one("a.card")["href"])


class NpmColParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("h3", {"class": "card-title"}).get_text()

    def get_date(self, *args, **kwargs) -> str | None:
        return None

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "card-content-bottom"}).get_text()

    def get_figure(self, *args, **kwargs) -> str | None:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")

        figure_url = "{}{}".format(target_domain, self.item.select_one("figure.card-image img")["data-src"])

        return self.clean_figure_url(figure_url)

    def clean_figure_url(self, o_url):
        u = urlparse(o_url)
        query = parse_qs(u.query, keep_blank_values=True)
        for word in {"w", "h"}:
            query.pop(word, None)
        u = u._replace(query=urlencode(query, True))
        return urlunparse(u)

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        div = self.item.find("div", {"class": "card-tags"})
        tags = div.get_text(strip=True)
        tags = [t.strip().replace("\u3000", "") for t in tags.split("#") if t.strip()]
        return tags

    def get_source_url(self, *args, **kwargs) -> str | None:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")

        return "{}{}".format(target_domain, self.item.select_one("a.card")["href"])


class NpmPreviewParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("a").get("title").strip()

    def get_date(self, *args, **kwargs) -> str | None:
        title = self.item.find("h3", {"class": "card-title-underline"})
        if title is None:
            return None
        date = title.next_element.next_element.next_element
        if date is None:
            return None
        return date.get_text().strip().replace("~", " ~ ")

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "card-content-bottom"}).get_text()

    def get_figure(self, *args, **kwargs) -> str | None:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")

        figure_url = "{}{}".format(target_domain, self.item.select_one("figure.card-image img")["data-src"])

        return self.clean_figure_url(figure_url)

    def clean_figure_url(self, o_url):
        u = urlparse(o_url)
        query = parse_qs(u.query, keep_blank_values=True)
        for word in {"w", "h"}:
            query.pop(word, None)
        u = u._replace(query=urlencode(query, True))
        return urlunparse(u)

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        div = self.item.find("div", {"class": "card-tags"})
        tags = div.get_text(strip=True)
        tags = [t.strip().replace("\u3000", "") for t in tags.split("#") if t.strip()]
        return tags

    def get_source_url(self, *args, **kwargs) -> str | None:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(target_domain, self.item.find("a").get("href"))


class SouthNpmParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def t(self, date_str: str) -> str:
        y, m, d = date_str.split("-")
        n_y = to_ad_year(int(y))
        return f"{n_y}-{m}-{d}"

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("a").get("title").strip()

    def get_date(self, *args, **kwargs) -> str | None:
        start, end = self.item.select("div.kf_imglist_time > span")
        start_str = start.get_text(strip=True)
        end_str = end.get_text(strip=True)

        if end_str:
            return f"{self.t(start_str)} ~ {self.t(end_str)}"

        return f"{self.t(start_str)} ~ "

    def get_address(self, *args, **kwargs) -> str | None:
        address = self.item.find("div", {"class": "remarks_ic-map"}).get_text(strip=True)
        if "S" in address and "F" in address:
            return "南部院區 " + address
        return self.item.find("div", {"class": "remarks_ic-map"}).get_text(strip=True)

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https://south.npm.gov.tw/" + self.item.find(
            "img",
        ).get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        tags = self.item.select("div.mg_b-nuit > span")
        return [tag.get_text(strip=True) for tag in tags]

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://south.npm.gov.tw/" + self.item.find("a").get("href")
