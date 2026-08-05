import datetime
import re

from selectolax.lexbor import LexborNode

from helpers.parse_helper import ParseInit


class PTAMParse(ParseInit):
    def __init__(self, item: LexborNode):
        self.item = item

    def get_title(self, *args, **kwargs) -> str | None:
        return self.item.css_first("span.txt47").text(strip=True)

    def get_date(self, *args, **kwargs) -> str | None:
        raw_date = self.item.css_first("samp").text(strip=True)

        parts = raw_date.split("~")
        if len(parts) != 2:
            return None

        raw_start, raw_end = parts[0].strip(), parts[1].strip()

        start_match = re.search(r"(?P<year>\d{4})[-/](?P<month>\d{1,2})[-/](?P<day>\d{1,2})", raw_start)
        if start_match is None:
            return None
        start_date = datetime.date(
            int(start_match.group("year")),
            int(start_match.group("month")),
            int(start_match.group("day")),
        )

        end_with_year = re.search(r"(?P<year>\d{4})[-/](?P<month>\d{1,2})[-/](?P<day>\d{1,2})", raw_end)
        if end_with_year:
            end_date = datetime.date(
                int(end_with_year.group("year")),
                int(end_with_year.group("month")),
                int(end_with_year.group("day")),
            )
        else:
            end_no_year = re.search(r"(?P<month>\d{1,2})[-/](?P<day>\d{1,2})", raw_end)
            if end_no_year is None:
                return None
            end_date = datetime.date(
                start_date.year,
                int(end_no_year.group("month")),
                int(end_no_year.group("day")),
            )

        return f"{start_date.isoformat()} ~ {end_date.isoformat()}"

    def get_address(self, *args, **kwargs) -> str | None:
        pass

    def get_figure(self, *args, **kwargs) -> str | None:
        return "https://ptam.ptcg.gov.tw/" + self.item.css_first("img").attributes.get("src")

    def get_tags(self, *args, **kwargs) -> list[str] | None:
        pass

    def get_source_url(self, *args, **kwargs) -> str | None:
        return "https://ptam.ptcg.gov.tw/" + self.item.css_first("a").attributes.get("href")
