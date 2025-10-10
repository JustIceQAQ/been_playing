import bs4

from helpers.parse_helper import ParseInit


class TcmParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("h2").get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        if (
            single_date := self.item.find("span", {"class": "date-display-single"})
        ) is not None:
            return single_date.get_text(strip=True).replace(".", "-")

        start_date = (
            self.item.find("span", {"class": "date-display-start"})
            .get_text(strip=True)
            .replace(".", "-")
        )
        end_date = (
            self.item.find("span", {"class": "date-display-end"})
            .get_text(strip=True)
            .replace(".", "-")
        )
        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.find("img", {"class": "img-fluid"}).attrs["src"]

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return (
            "https://tcm.tainan.gov.tw"
            + self.item.find("a", {"class": "d-block"}).attrs["href"]
        )
