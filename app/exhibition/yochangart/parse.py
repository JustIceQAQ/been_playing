import bs4

from helpers.parse_helper import ParseInit


class YoChangArtParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        figure_caption = self.item.find("div", {"class": "figure_caption"})
        h2 = figure_caption.find("h2")
        return h2.get_text()

    def get_date(self, *args, **kwargs) -> str | None:
        figure_caption = self.item.find("div", {"class": "figure_caption"})
        p = figure_caption.find("p")
        if p is None:
            return None
        raw_start_date, raw_end_date = p.get_text().split("-")
        if len(raw_end_date.split(".")) == 2:
            s_year = raw_start_date.split(".")[0]
            raw_end_date = s_year + "." + raw_end_date

        ok_start_date = raw_start_date.replace(".", "-")
        ok_end_date = raw_end_date.replace(".", "-")
        return ok_start_date + " ~ " + ok_end_date

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https://museum.ntua.edu.tw/" + self.item.find("img").get("src")

    def get_source_url(self, *args, **kwargs) -> str | None:
        figure_caption = self.item.find("div", {"class": "figure_caption"})
        a = figure_caption.find("a")
        return "https://museum.ntua.edu.tw/" + a.get("href")
