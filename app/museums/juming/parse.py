from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit


class JuMingParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.css_first("span.meMsg_MsgTitle").text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        return self.item.css_first("span.meMsg_MsgSubTitle").text(strip=True).replace("/", ".").replace("-", " ~ ")

    def get_address(self, *args, **kwargs) -> str | None:
        return self.item.css_first("div.meMsg_Content").text(strip=True)

    def get_figure(self, *args, **kwargs) -> str | None:
        return self.item.css_first("img.ImgAlignCenter").attributes.get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        xml_id = self.item.css_first("a").attributes.get("href").split("=")[1]
        return f"https://www.juming.org.tw/mainssl/modules/MySpace/BlogInfo.php?xmlid={xml_id}"
