import bs4

from helpers.parse_helper import ParseInit


class ArtEmperorParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("h2").get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        p = self.item.find("p").get_text(strip=True)
        return p.split("｜")[0].split("：")[1].strip()

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item.find("h3").get_text(strip=True)

    def get_figure(self, *args, **kwargs) -> str | None:
        style = self.item.find("div", {"class": "pic"}).get("style")
        return style.split("url(")[1].split(");")[0]

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.find("h2").parent.get("href")
