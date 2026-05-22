import asyncio
import datetime
from typing import cast

from selectolax.lexbor import LexborNode

from app.museums.afmc.parse import AfmcParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.selectolax import SelectolaxTranslation
from helpers.utils_helper import month_3

BASE_URL = "https://www.afmc.gov.tw"


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

    def set_information(self) -> Information:
        return Information(
            fullname="桃園展演中心",
            code_name="AfmcHall1",
            external_link=BASE_URL,
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.017555022836635, 121.29841018064276"),
                raw_coordinates="25.017555022836635, 121.29841018064276",
            ),
            location_code=Taiwan.taoyuan.taoyuan_68000010,
            venue_type=VenueType.EXPO_CENTER,
        )


class AfmcHall2Runner(AfmcBaseRunner):
    hall_code = "hall2"

    def set_information(self) -> Information:
        return Information(
            fullname="中壢藝術館",
            code_name="AfmcHall2",
            external_link=BASE_URL,
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="24.958508250916836, 121.22748825365926"),
                raw_coordinates="24.958508250916836, 121.22748825365926",
            ),
            location_code=Taiwan.taoyuan.zhongli_68000020,
            venue_type=VenueType.MUSEUM,
        )


class AfmcHall3Runner(AfmcBaseRunner):
    hall_code = "hall3"

    def set_information(self) -> Information:
        return Information(
            fullname="桃園光影文化館",
            code_name="AfmcHall3",
            external_link=BASE_URL,
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="24.999357351659583, 121.30748928249685"),
                raw_coordinates="24.999357351659583, 121.30748928249685",
            ),
            location_code=Taiwan.taoyuan.taoyuan_68000010,
            venue_type=VenueType.ART_MUSEUM,
        )


class AfmcHall4Runner(AfmcBaseRunner):
    hall_code = "hall4"

    def set_information(self) -> Information:
        return Information(
            fullname="桃園藝文廣場",
            code_name="AfmcHall4",
            external_link=BASE_URL,
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.017657555942453, 121.30002828249722"),
                raw_coordinates="25.017657555942453, 121.30002828249722",
            ),
            location_code=Taiwan.taoyuan.zhongli_68000020,
            venue_type=VenueType.ART_MUSEUM,
        )


class AfmcHall5Runner(AfmcBaseRunner):
    hall_code = "hall5"

    def set_information(self) -> Information:
        return Information(
            fullname="A8藝文中心",
            code_name="AfmcHall5",
            external_link=BASE_URL,
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.06063397917656, 121.36993362482592"),
                raw_coordinates="25.06063397917656, 121.36993362482592",
            ),
            location_code=Taiwan.taoyuan.guishan_68000070,
            venue_type=VenueType.ART_MUSEUM,
        )


class AfmcHall6Runner(AfmcBaseRunner):
    hall_code = "hall6"

    def set_information(self) -> Information:
        return Information(
            fullname="桃園陽光劇場",
            code_name="AfmcHall6",
            external_link=BASE_URL,
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.02441059026342, 121.21753328064304"),
                raw_coordinates="25.02441059026342, 121.21753328064304",
            ),
            location_code=Taiwan.taoyuan.dayuan_68000060,
            venue_type=VenueType.ART_MUSEUM,
        )


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await asyncio.gather(
        *[
            Runner().run(NoneCache(), NoneImageHosting())
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
