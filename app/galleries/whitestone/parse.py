import bs4

from helpers.parse_helper import ParseInit


class WhiteStoneParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("div", {"class": "wsg-exhibition-label__title"}).get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        p_tag = self.item.find("div", {"class": "wsg-exhibition-label__description"}).find("p")
        if p_tag is None:
            return None
        details = list(p_tag.stripped_strings)
        if len(details) >= 2:
            date_range = details[1]
            start_date, end_date = date_range.split("-")

            start_date = start_date.strip()
            end_date = end_date.strip()

            s_y, _, _ = start_date.split(".")
            if len(end_date.split(".")) != 3:
                e_m, e_d = end_date.split(".")
                ok_end_date = f"{s_y}-{e_m}-{e_d}"
            else:
                ok_end_date = end_date.replace(".", "-")
            ok_start_date = start_date.replace(".", "-")
            return f"{ok_start_date} ~ {ok_end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        p_tag = self.item.find("div", {"class": "wsg-exhibition-label__description"}).find("p")
        if p_tag is None:
            return None
        details = list(p_tag.stripped_strings)
        if len(details) >= 2:
            location = details[0]
            return location

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https:" + self.item.find("img").get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://www.whitestone-gallery.com" + self.item.find("a").get("href")
