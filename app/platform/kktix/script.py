import asyncio
import datetime as dt
import json
import urllib.parse
from typing import cast

import bs4
from dateutil.relativedelta import relativedelta
from wreq import Proxy

from app.platform.kktix.parse import KKTixParse
from configs.settings import get_settings
from helpers.crawler.wreq.helper import WReqAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import get_date, month_3


def within_two_months() -> tuple[dt.datetime, dt.datetime]:
    today = get_date.time_now
    today_add_2_months = (today + relativedelta(months=2)) - dt.timedelta(days=1)
    return today, today_add_2_months


class KKTixRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = KKTixParse
    target_url = (
        "https://kktix.com/events?"
        "utf8=%E2%9C%93"
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
            venue_type=VenueType.PLATFORM,
        )

    async def fetch_response(self):
        today, today_add_2_months = within_two_months()
        start_at = urllib.parse.quote(today.strftime("%Y/%m/%d"), safe="")
        end_at = urllib.parse.quote(today_add_2_months.strftime("%Y/%m/%d"), safe="")
        responses = []
        runtime_settings = get_settings()
        proxies = None
        if runtime_settings.PROXY_POOL is not None:
            proxies = [Proxy.all(runtime_settings.PROXY_POOL)]
        async with WReqAsyncClient(
            proxies=proxies,
        ) as client:
            page = 1
            while True:
                response = await client.get(
                    self.target_url.format(start_at=start_at, end_at=end_at, page=page),
                )
                if not response.status.is_success():
                    break
                this_response_text = await response.text()
                translation_data = self.translation().translation_to_object(this_response_text)
                if (translation_data is None) or (
                    translation_data.select_one("div[data-react-class='SearchWrapper']") is None
                ):
                    break
                responses.append(this_response_text)
                page += 1

        return responses

    async def fetch_parsed(self):
        items = []
        parsers = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        for parsed in parsers:
            if parsed is None:
                continue
            data = parsed.select_one("div[data-react-class='SearchWrapper']").get("data-react-props")
            items.extend(json.loads(data).get("data", []))
        return items


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await KKTixRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
