from helpers.parse_helper import ParseInit

from selectolax.lexbor import LexborNode


class AAAArchivesParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.css_first("a").attributes.get("title").strip()

    def get_date(self, *args, **kwargs) -> str | None:
        i_calendar = self.item.css_first("i.i_calendar")
        if i_calendar:
            raw_date = i_calendar.parent.child
            if raw_date:
                return raw_date.text(strip=True).replace("/", "-")

    def get_address(self, *args, **kwargs) -> str | None:
        title = self.item.css_first("a").attributes.get("title").strip()
        if "行動展" in title:
            return "線上展"
        return "新北市林口區檔案館路1號 (已洽電詢問，展覽皆在林口區新館)"

    def get_figure(self, *args, **kwargs) -> str | None:
        img = self.item.css_first("img")
        if img:
            src = img.attributes.get("src")
            return "https://aaa.archives.tw" + src

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        i_man = self.item.css_first("i.i_man")
        if i_man:
            raw_man = i_man.parent.child
            if raw_man:
                return raw_man.text(strip=True).split(",")

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.css_first("a").attributes.get("href")
