from helpers.parse_helper import ParseInit

from selectolax.lexbor import LexborNode


class HistorySinicaParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.css_first("div.title a").text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        div_time = self.item.css_first("div.time")
        time_text = div_time.text(strip=True)
        if "開始日期" in time_text:
            return time_text.replace("開始日期", "").strip() + " ~"
        return self.item.css_first("div.time").text(strip=True).replace("至", "~")

    def get_address(self, *args, **kwargs) -> str | None:
        div_location = self.item.css_first("div.location")
        if div_location:
            return div_location.text(strip=True)

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https://museum.sinica.edu.tw/" + self.item.css_first("img").attributes.get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://museum.sinica.edu.tw/" + self.item.css_first("div.title a").attributes.get("href")
