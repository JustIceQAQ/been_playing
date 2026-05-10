import asyncio
from typing import cast

from app.museums.tfam.parse import TFamParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class TFamRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = TFamParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.zhongshan_63000040,
            fullname="臺北市立美術館",
            code_name="TFam",
            external_link="https://www.tfam.museum/Exhibition/Exhibition.aspx?ddlLang=zh-tw",
            branch_coordinates=Coordinate(raw_coordinates="25.07240807900826, 121.5244680697716"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(
            origin="https://www.tfam.museum",
            referer="https://www.tfam.museum/Exhibition/Exhibition.aspx?ddlLang=zh-tw",
            host="www.tfam.museum",
            x_requested_with="XMLHttpRequest",
            other_headers={
                "Content-Type": "application/json; charset=UTF-8",
            },
        )
        cookies = generate_cookies(need_asp_net_session_id=True)
        async with HttpxAsyncClient(headers=headers) as client:
            tasks = [
                client.post(
                    "https://www.tfam.museum/ashx/Exhibition.ashx?ddlLang=zh-tw",
                    json={"JJMethod": "GetEx", "Type": str(i)},
                    cookies=cookies,
                )
                for i in range(1, 3)
            ]
            responses = await asyncio.gather(*tasks)
        return [response.json() for response in responses]

    async def fetch_parsed(self):
        data = []
        parsers = cast(list[dict], await super().fetch_parsed())
        for parsed in parsers:
            data.extend(parsed.get("Data", []))
        return data

    async def fetch_items(self, *args, **kwargs):
        return await super().fetch_items(target_domain="https://www.tfam.museum")


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image.none.helper import NoneImage

    await TFamRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
