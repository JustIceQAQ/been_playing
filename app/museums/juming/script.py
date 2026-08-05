import asyncio
import secrets
from typing import cast

from selectolax.lexbor import LexborNode

from app.museums.juming.parse import JuMingParse
from helpers.crawler.niquests.helper import NiquestsAsyncSession
from helpers.headers_helper import generate_cookies, generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3


class JuMingRunner(RunnerInit):
    translation = SelectolaxTranslation
    use_parse = JuMingParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.new_taipei.jinshan_65000270,
            fullname="朱銘美術館",
            code_name="JuMing",
            external_link="https://www.juming.org.tw/",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.246492169720533, 121.61118935623358"),
                raw_coordinates="25.246492169720533, 121.61118935623358",
            ),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers(host="www.juming.org.tw")
        cookies = generate_cookies(other_cookies={"w62ns_session": secrets.token_hex(13)})
        async with NiquestsAsyncSession(headers=headers) as client:
            response = await client.get(
                "https://www.juming.org.tw/mainssl/modules/MySpace/BlogList.php?sn=ec&pn=1&cn=ZC543803", cookies=cookies
            )
        return response.text

    async def fetch_parsed(self):
        parsed = cast(LexborNode, await super().fetch_parsed())
        items = parsed.css("div.dataBlogList.MsgInfoData")
        return items


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await JuMingRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
