from helpers.parse_helper import ParseInit


from selectolax.lexbor import LexborNode


class CCAMParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.css_first("title").text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        start_date = self.item.css_first("div[title='開始日期'] div.p span").text(strip=True)
        end_date = self.item.css_first("div[title='結束日期'] div.p span").text(strip=True)

        def roc_to_ad(roc_date: str) -> str:
            year, month, day = roc_date.split("-")
            return f"{int(year) + 1911}-{month}-{day}"

        return f"{roc_to_ad(start_date)} ~ {roc_to_ad(end_date)}"

    ADDRESS_TITLES = ["地點", "展覽地點"]

    def get_address(self, *args, **kwargs) -> str | None:
        node = next(
            (
                self.item.css_first(f"div[title='{t}'] div.p span")
                for t in self.ADDRESS_TITLES
                if self.item.css_first(f"div[title='{t}'] div.p span")
            ),
            None,
        )
        return node.text(strip=True) if node else None

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.css_first("div.list-pic img").attributes.get("src")

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.css_first("meta[property='og:url']").attributes.get("content")
