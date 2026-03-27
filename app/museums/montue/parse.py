import bs4

from helpers.parse_helper import ParseInit
from urllib.parse import urlparse, urlunparse, quote


class MoNTUEParse(ParseInit):
    def __init__(self, item: bs4.element.Tag):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        title = self.item.find("title").get_text(strip=True)
        return title.rsplit("|")[0].strip()

    def get_date(self, *args, **kwargs) -> str | None:
        strong_tag = self.item.find("strong", string="展期")
        if strong_tag:
            next_content = strong_tag.next_sibling
            if next_content:
                result = next_content.strip()
                raw_date = result.replace("｜", "").strip()
                return raw_date.replace("-", " ~ ").replace(".", "-")

    def get_address(self, *args, **kwargs) -> str | None:
        strong_tag = self.item.find("strong", string="地點")
        if strong_tag:
            next_content = strong_tag.next_sibling
            if next_content:
                result = next_content.strip()
                return result.replace("｜", "").strip()

    def get_figure(self, *args, **kwargs) -> str | None:
        original_url = self.item.find("meta", {"name": "twitter:image"}).get("content")
        parsed_url = urlparse(original_url)
        encoded_path = quote(parsed_url.path)
        safe_url = urlunparse(parsed_url._replace(path=encoded_path))
        return safe_url

    def get_tags(self, *args, **kwargs) -> list[str | None] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        url = self.item.find("meta", {"property": "og:url"}).get("content")
        return url
