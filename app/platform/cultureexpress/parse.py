import bs4

from helpers.parse_helper import ParseInit


def roc_to_ad(roc_date_str):
    roc_year, month, day = map(int, roc_date_str.strip().split("/"))
    ad_year = roc_year + 1911
    return f"{ad_year:04d}-{month:02d}-{day:02d}"


class CultureExpressParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.select_one("div.rd-tit").get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        p = self.item.find("p", class_="card-date")
        text_nodes = [t.strip() for t in p.contents if t.name is None and t.strip()]
        if len(text_nodes) == 2:
            return roc_to_ad(text_nodes[0]) + " ~ " + roc_to_ad(text_nodes[1])

    def get_address(self, *args, **kwargs) -> str | None:
        card_text_list = self.item.select("ul.card-text-list li")
        for text_node in card_text_list:
            if ("活動地點" in text_node.text) and ("http" not in text_node.text):
                return text_node.text.replace("活動地點：", "")

    def get_figure(self, *args, **kwargs) -> str | None:
        return (
            "https://cultureexpress.taipei"
            + self.item.select_one("figure > img").attrs["src"]
        )

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://cultureexpress.taipei" + self.item.select_one("a").attrs["href"]
