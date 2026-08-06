import asyncio
import datetime
from typing import TYPE_CHECKING, cast

from selectolax.lexbor import LexborNode

from app.museums.afmc.information import (
    AfmcHall1Information,
    AfmcHall2Information,
    AfmcHall3Information,
    AfmcHall4Information,
    AfmcHall5Information,
    AfmcHall6Information,
)
from app.museums.afmc.parse import AfmcParse
from helpers.crawler.headers_helper import generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3

BASE_URL = "https://www.afmc.gov.tw"

if TYPE_CHECKING:
    from helpers.storage.helper import Information


class AfmcBaseRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = AfmcParse
    hall_code: str
    retry_on_empty = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    async def fetch_response(self):
        today = datetime.date.today()
        end = today + datetime.timedelta(days=180)
        start_str = today.strftime("%Y/%m/%d")
        end_str = end.strftime("%Y/%m/%d")
        url = f"{BASE_URL}/Activity?c3={self.hall_code}&start={start_str}&end={end_str}&c5=performance2&k="
        headers = generate_headers(host="www.afmc.gov.tw", referer=BASE_URL)
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(url)
            response.raise_for_status()
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        return parsed.css("a[href*='/Activity_detail/']")


class AfmcHall1Runner(AfmcBaseRunner):
    hall_code = "hall1"

    def set_information(self) -> "Information":
        return AfmcHall1Information.get_information()


class AfmcHall2Runner(AfmcBaseRunner):
    hall_code = "hall2"

    def set_information(self) -> "Information":
        return AfmcHall2Information.get_information()


class AfmcHall3Runner(AfmcBaseRunner):
    hall_code = "hall3"

    def set_information(self) -> "Information":
        return AfmcHall3Information.get_information()


class AfmcHall4Runner(AfmcBaseRunner):
    hall_code = "hall4"

    def set_information(self) -> "Information":
        return AfmcHall4Information.get_information()


class AfmcHall5Runner(AfmcBaseRunner):
    hall_code = "hall5"

    def set_information(self) -> "Information":
        return AfmcHall5Information.get_information()


class AfmcHall6Runner(AfmcBaseRunner):
    hall_code = "hall6"

    def set_information(self) -> "Information":
        return AfmcHall6Information.get_information()


async def main():
    from helpers.cache import none_cache
    from helpers.image_hosting import none_image_hosting

    await asyncio.gather(
        *[
            Runner().run(none_cache, none_image_hosting)
            for Runner in [
                AfmcHall1Runner,
                AfmcHall2Runner,
                AfmcHall3Runner,
                AfmcHall4Runner,
                AfmcHall5Runner,
                AfmcHall6Runner,
            ]
        ]
    )


if __name__ == "__main__":
    asyncio.run(main())
