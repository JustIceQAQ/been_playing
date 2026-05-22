import asyncio
from typing import cast

import bs4

from app.museums.mocataipei.parse import MoCaTaipeiParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate, GoogleMaps, OpenStreetMap, Wiki, GeoPoint
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class MoCaTaipeiRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = MoCaTaipeiParse
    output_ics = True
    output_rss = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.datong_63000060,
            fullname="台北當代藝術館",
            code_name="MoCaTaipei",
            external_link="https://www.mocataipei.org.tw/tw/ExhibitionAndEvent",
            branch_coordinates=Coordinate(
                location_code=Taiwan.taipei.datong_63000060,
                address="103臺北市大同區建泰里長安西路39號",
                google_maps=GoogleMaps(plus_code="3G29+8H 建泰里 臺北市大同區"),
                open_street_map=OpenStreetMap(
                    osm_url="https://www.openstreetmap.org/way/217690234",
                    tourism="museum",
                ),
                wiki=Wiki(
                    wikidata="Q699040",
                    wikipedia="zh:台北當代藝術館",
                ),
                geo_point=GeoPoint(raw_coordinates="25.05101850889424, 121.51900878326302"),
                raw_coordinates="25.05101850889424, 121.51900878326302",
            ),
            venue_type=VenueType.ART_MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        target_url = [
            "https://www.mocataipei.org.tw/tw/ExhibitionAndEvent",
            "https://www.mocataipei.org.tw/tw/ExhibitionAndEvent/Exhibitions/Upcoming",
        ]
        async with HttpxAsyncClient(headers=headers) as client:
            tasks = [client.get(url) for url in target_url]
            tasks_response = await asyncio.gather(*tasks)
        return [task.text for task in tasks_response]

    async def fetch_parsed(self):
        parsers = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        items_dataset = []
        for parsed in parsers:
            if runtime_element := parsed.select("div.listFrameBox div.list"):
                items_dataset.extend(runtime_element)
        return items_dataset

    async def fetch_items(self, *args, **kwargs):
        return await super().fetch_items(target_domain="https://www.mocataipei.org.tw")


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image_hosting.none.helper import NoneImageHosting

    await MoCaTaipeiRunner().run(NoneCache(), NoneImageHosting())


if __name__ == "__main__":
    asyncio.run(main())
