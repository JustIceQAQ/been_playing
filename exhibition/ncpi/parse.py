import bs4
import cssutils

from helper.parse_helper import ParseInit


class NCPIParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str:
        return self.item.get("title")

    def get_date(self, *args, **kwargs) -> str:
        raw_date_string = self.item.select_one("div.label >ul > li >span > i.mark").get_text()
        split_date = raw_date_string.split("~")
        clean_split_date = [i for i in split_date if i]
        if len(clean_split_date) == 2:
            start_date, end_date = split_date
            start_date = start_date.strip()
            end_date = end_date.strip()
            if (len((start_date_data := start_date.split("-"))) == 3
                    and len((end_date_data := end_date.split("-"))) == 3
            ):
                raw_date_string = f"{start_date} ~ {end_date}"
        else:
            raw_date_string = raw_date_string.strip()
            raw_date_string = f"{raw_date_string} ~" if split_date[1] == "" else raw_date_string
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
