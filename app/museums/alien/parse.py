import bs4

from helpers.parse_helper import ParseInit


class AlienParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.select_one("h2.topTitle > a").get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        tags = self.item.select("span.tag")
        if len(tags) != 1:
            return None

        tag = tags[0].get_text(strip=True).strip()
        if tag in "常設展覽":
            return None

        data = tag.split("-")
        data2 = tag.split("~")

        use_data = None

        if len(data) == 2:
            use_data = data
        elif len(data2) == 2:
            use_data = data2
        else:
            return use_data

        start_date, end_date = use_data

        start_date = start_date.strip()
        end_date = end_date.strip()

        return f"{start_date} ~ {end_date}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        style = self.item.find("div", {"role": "img"}).get("style")
        url = style.split("')")[0].split("url('")[1]
        return "https://www.alien.com.tw" + url

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        tags = self.item.select("span.tag")
        return [tag.get_text(strip=True) for tag in tags]

    def get_source_url(self, *args, **kwargs) -> str | None:
        href = self.item.select_one("h2.topTitle > a").get("href")
        return "https://www.alien.com.tw" + href
