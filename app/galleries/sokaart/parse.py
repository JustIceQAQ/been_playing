import bs4

from helpers.parse_helper import ParseInit


class SoKaArtParse(ParseInit):
    def __init__(self, item: bs4.element.Tag | dict):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.find("h3", {"class": "title"}).get_text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        time = self.item.find("p", {"class": "time"}).get_text(strip=True)
        s_time, e_time = time.split("-")
        s_time: str = s_time.strip()
        e_time: str = e_time.strip()

        if len(e_time.split(".")) != 3:
            s_t_year = s_time.split(".")[0]
            e_time = s_t_year + e_time

        s_time = s_time.replace(".", "-")
        e_time = e_time.replace(".", "-")

        return f"{s_time} ~ {e_time}"

    def get_address(self, *args, **kwargs) -> str | None:
        text = self.item.find("div", {"class": "text"}).get_text(strip=True)
        if "索卡藝術" in text:
            other_text = text.split("索卡藝術")[1]
            return "索卡藝術" + other_text[:3]

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https://soka-art.com" + self.item.find("img").get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://soka-art.com" + self.item.find("h3", {"class": "title"}).find(
            "a"
        ).get("href")
