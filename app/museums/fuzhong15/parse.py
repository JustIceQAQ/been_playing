from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit


class FuZhong15Parse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        title = self.item.css_first("div.img_bg").next.next.css_first("strong")
        if title is not None:
            return title.text(strip=True)
        return self.item.css_first("h2.PageTitle").text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        pass

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.css_first("div.img_bg img").attributes.get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return self.item.css_first("meta[property='og:Url']").attributes.get("content")
