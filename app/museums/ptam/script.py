import asyncio

from typing import cast
from app.museums.ptam.parse import PTAMParse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan

from helpers.utils_helper import month_3


from helpers.crawler.niquests.helper import NiquestsAsyncSession


from selectolax.lexbor import LexborNode
from helpers.translation.selectolax import SelectolaxTranslation


class PTAMRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = PTAMParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.pingtung.pingtung_10013010,
            fullname="屏東美術館",
            code_name="PTAM",
            external_link="https://ptam.ptcg.gov.tw/",
            branch_coordinates=Coordinate(raw_coordinates="22.674969712813024, 120.48993190095096"),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        cookies = generate_cookies(need_phpsessid=True)
        async with NiquestsAsyncSession(headers=headers) as client:
            response = await client.get("https://ptam.ptcg.gov.tw/period.php", cookies=cookies)
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        data = parsed.css("article div.nav12")
        return data


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await PTAMRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
