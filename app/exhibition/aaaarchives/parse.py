from justhtml import JustHTML

from helpers.parse_helper import ParseInit


class AAAArchivesParse(ParseInit):
    def __init__(self, item: JustHTML):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.query("a")[0].attrs["title"].strip()

    def get_date(self, *args, **kwargs) -> str | None:
        i_calendar = self.item.query("i.i_calendar")[0]
        if i_calendar:
            raw_date = i_calendar.parent.children[1]
            if raw_date:
                return raw_date.to_text(strip=True).replace("/", "-")

    def get_address(self, *args, **kwargs) -> str | None:
        title = self.item.query("a")[0]

        title = title.attrs["title"].strip()
        if "行動展" in title:
            return "線上展"
        return "新北市林口區檔案館路1號 (已洽電詢問，展覽皆在林口區新館)"

    def get_figure(self, *args, **kwargs) -> str | None:
        img = self.item.query("img")[0]
        if img:
            src = img.attrs["src"]
            return "https://aaa.archives.tw" + src

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        i_man = self.item.query("i.i_man")[0]
        if i_man:
            raw_man = i_man.parent.children[1]
            if raw_man:
                return raw_man.to_text(strip=True).split(",")

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.query("a")[0].attrs["href"]
