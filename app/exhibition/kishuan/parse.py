from justhtml import JustHTML

from helpers.parse_helper import ParseInit


class KiShuAnParse(ParseInit):
    def __init__(self, item: JustHTML):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        title: JustHTML = self.item.query("h3.title")[0]
        return title.to_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        date: JustHTML = self.item.query("div.date")[0]
        return date.to_text(strip=True).replace("至", " ~ ")

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        img: JustHTML = self.item.query("img.img-responsive")[0]
        return "https://kishuan.org.tw" + img.attrs["src"]

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        a: JustHTML = self.item.query("a")[0]
        return "https://kishuan.org.tw/" + a.attrs["href"]
