import asyncio
import datetime as dt
import json
import urllib.parse

import bs4
from dateutil.relativedelta import relativedelta

from app.platform.kktix.parse import KKTixParse
from helpers.cache.none import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import datetime_now, month_3


def within_two_months() -> tuple[dt.datetime, dt.datetime]:
    today = datetime_now()
    today_add_2_months = (today + relativedelta(months=2)) - dt.timedelta(days=1)
    return today, today_add_2_months


class KKTixRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = KKTixParse
    target_url = (
        "https://kktix.com/events?"
        "utf8=✓"
        "&search="
        "&max_price="
        "&min_price="
        "&start_at={start_at}"
        "&end_at={end_at}"
        "&event_tag_ids_in=4"
        "&page={page}"
    )

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="KKTix",
            code_name="KKTix",
            external_link="https://kktix.com/events?utf8=%E2%9C%93&event_tag_ids_in=4",
        )

    async def fetch_response(self):
        headers = {
            **get_header(),
            "referer": "https://kktix.com/",
        }

        today, today_add_2_months = within_two_months()
        start_at = urllib.parse.quote(today.strftime("%Y/%m/%d"), safe="")
        end_at = urllib.parse.quote(today_add_2_months.strftime("%Y/%m/%d"), safe="")
        responses = []
        async with HttpxAsyncClient(headers=headers) as client:
            page = 1
            while True:
                response = await client.get(
                    self.target_url.format(start_at=start_at, end_at=end_at, page=page)
                )
                if (
                    self.translation()
                    .translation_to_object(response.text)
                    .select_one("div[data-react-class='SearchWrapper']")
                    is None
                ):
                    break
                responses.append(response.text)
                page += 1

        return responses

    async def fetch_parsed(self):
        items = []
        parsers: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        for parsed in parsers:
            data = parsed.select_one("div[data-react-class='SearchWrapper']").get(
                "data-react-props"
            )
            items.extend(json.loads(data).get("data", []))
        return items


async def main():
    await KKTixRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
