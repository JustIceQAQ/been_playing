import asyncio

import bs4

from app.galleries.whitestone.parse import WhiteStoneParse
from helpers.headers_helper import get_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class WhiteStoneRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = WhiteStoneParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="白石畫廊",
            code_name="WhiteStone",
            external_link="https://www.whitestone-gallery.com/zh-hant",
            branch_coordinates=Coordinate(raw_coordinates="25.081886335785196, 121.5655333509274"),
        )

    async def fetch_response(self):
        urls = [
            "https://www.whitestone-gallery.com/zh-hant/blogs/exhibitions/tagged/location_taipei+current",
            "https://www.whitestone-gallery.com/zh-hant/blogs/exhibitions/tagged/location_taipei+upcoming"
        ]
        headers = get_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            responses = await asyncio.gather(
                *[client.get(url)
                  for url in urls]
            )
        return [response.text for response in responses]

    async def fetch_parsed(self):
        parsed: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        datas = []
        for p in parsed:
            datas.extend(p.select("div.wsg-exhibition-card"))
        return datas


async def main():
    await WhiteStoneRunner().run(NoneCache(), NoneImage())


if __name__ == '__main__':
    asyncio.run(main())
