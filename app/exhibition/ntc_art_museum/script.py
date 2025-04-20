import asyncio

import bs4

from app.exhibition.ntc_art_museum.parse import (
    NtcArtMuseumMainParse,
    NtcArtMuseumOtherParse,
)
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import ExhibitionItem, Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class NtcArtMuseumRunner(RunnerInit):
    translation = BeautifulSoupTranslation

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="新北市美術館",
            code_name="NtcArtMuseum",
            external_link="https://ntcart.museum/exhibition",
        )

    async def fetch_response(self):
        headers = get_header()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://ntcart.museum/exhibition")
        return response.text

    async def fetch_parsed(self) -> dict:
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        art_content_other = parsed.select("div.art-content-other.ex-group > a")
        main_exhibition = parsed.select("div.main-pic > a")
        coming_soon = parsed.select("div.art-content-other.comingSoon > a")

        return {
            "art_content_other": art_content_other,
            "main_exhibition": main_exhibition,
            "coming_soon": coming_soon,
        }

    def _sub_fetch_items(self, parsed_, use_parse, *args, **kwargs) -> list:
        sub_exhibition_items = []
        for item in parsed_:
            data = use_parse(item).parse_to_base_model(ExhibitionItem, *args, **kwargs)
            if data.source_url is None:
                continue
            sub_exhibition_items.append(data)
        return sub_exhibition_items

    async def fetch_items(self, *args, **kwargs):
        exhibition_items = []
        runtime_parsed = self.parsed_
        exhibition_items.extend(
            self._sub_fetch_items(
                runtime_parsed["art_content_other"],
                NtcArtMuseumOtherParse,
                target_domain="https://ntcart.museum",
            )
        )
        exhibition_items.extend(
            self._sub_fetch_items(
                runtime_parsed["main_exhibition"],
                NtcArtMuseumMainParse,
                target_domain="https://ntcart.museum",
            )
        )

        exhibition_items.extend(
            self._sub_fetch_items(
                runtime_parsed["coming_soon"],
                NtcArtMuseumOtherParse,
                target_domain="https://ntcart.museum",
            )
        )

        return exhibition_items


async def main():
    await NtcArtMuseumRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
