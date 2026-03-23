import bs4

from helpers.parse_helper import ParseInit


class XiZhiTangParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("h2").get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        p = self.item.find("p").get_text(strip=True)
        if "日期" in p:
            return p.replace("日期：", "").strip()

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        style = self.item.find("span", {"class": "bg"}).get("style")
        return style.split(":url(")[1][:-2]

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.find("a").get("href")
