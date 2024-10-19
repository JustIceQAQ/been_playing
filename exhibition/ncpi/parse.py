import bs4

from helper.parse_helper import ParseInit


class NCPIParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.get("title")

    def get_date(self, *args, **kwargs) -> str:
        raw_date_string = self.item.select_one(
            "div.label >ul > li >span > i.mark"
        ).get_text()
        split_date = raw_date_string.split("~")
        if len(split_date) == 2:
            start_date, end_date = split_date
            if end_date == "":
                raw_date_string = raw_date_string.strip()
            else:
                start_date = start_date.strip()
                end_date = end_date.strip()
                if len(start_date.split("-")) == 3 and len(end_date.split("-")) == 3:
                    raw_date_string = f"{start_date} ~ {end_date}"
        else:
            raw_date_string = raw_date_string.strip()
        return raw_date_string

    def get_address(self, *args, **kwargs) -> str:
        return self.item.select_one("div.place >ul > li >span > i.mark").get_text()

    def get_figure(self, *args, **kwargs) -> str:
        img = self.item.find("img")

        return img.get("src")

    def get_source_url(self, *args, **kwargs) -> str:
        target_domain = kwargs.get("target_domain", None)
        if target_domain is None:
            raise ValueError("請提供 TARGET_DOMAIN")
        return "{}{}".format(target_domain, self.item.get("href"))
