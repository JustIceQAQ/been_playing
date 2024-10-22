from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import bs4

from helper.parse_helper import ParseInit


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
        return self.item.find("h3", {"class": "card-title"}).get_text()

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
