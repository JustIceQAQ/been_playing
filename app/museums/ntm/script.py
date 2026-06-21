import asyncio
from collections import defaultdict
from itertools import chain
from typing import cast

import bs4

from app.museums.ntm.parse import NtmParse, all_branch
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.coordinate import Coordinate, GoogleMaps, GeoPoint
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class NtmRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NtmParse
    use_suffix_item_from_file_func = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="國立臺灣博物館",
            code_name="Ntm",
            external_link="https://www.ntm.gov.tw/Default.aspx",
            location_code=Taiwan.taipei.zhongzheng_63000050,
            branch_coordinates=[
                Coordinate(
                    location_code=Taiwan.taipei.zhongzheng_63000050,
                    google_maps=GoogleMaps(plus_code="2GV8+42 黎明里 臺北市中正區"),
                    name="本館",
                    raw_coordinates="25.042991302660226, 121.5151621120989",
                    geo_point=GeoPoint(
                        raw_coordinates="25.042991302660226, 121.5151621120989",
                    ),
                ),
                Coordinate(
                    location_code=Taiwan.taipei.zhongzheng_63000050,
                    name="古生物館",
                    raw_coordinates="25.043788780293, 121.51440168326278",
                    geo_point=GeoPoint(
                        raw_coordinates="25.043788780293, 121.51440168326278",
                    ),
                ),
                Coordinate(
                    location_code=Taiwan.taipei.datong_63000060,
                    name="鐵道部園區",
                    raw_coordinates="25.048869075417418, 121.5113360427876",
                    geo_point=GeoPoint(
                        raw_coordinates="25.048869075417418, 121.5113360427876",
                    ),
                ),
                Coordinate(
                    location_code=Taiwan.taipei.zhongzheng_63000050,
                    name="南門館",
                    raw_coordinates="25.033613597291687, 121.51583661209861",
                    geo_point=GeoPoint(
                        raw_coordinates="25.033613597291687, 121.51583661209861",
                    ),
                ),
            ],
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        headers = generate_headers()
        urls_template = "https://www.ntm.gov.tw/News_actives.aspx?n={n}&sms={sms}&_CSN={csn}&page=1&PageSize=50"
        tasks = []
        async with HttpxAsyncClient(headers=headers) as client:
            for branch in all_branch:
                for path_query_data in branch:
                    tasks.append(
                        client.get(
                            urls_template.format(
                                n=path_query_data.n,
                                sms=path_query_data.sms,
                                csn=path_query_data.csn,
                            ),
                        )
                    )
            responses = await asyncio.gather(*tasks)

        return [response.text for response in responses]

    async def fetch_parsed(self) -> list:
        parsers = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        return list(
            chain.from_iterable(
                selected_one.select("ul[data-child] > li[data-index] > div.area-essay")
                for parser in parsers
                if (selected_one := parser.select_one("#CCMS_Content")) is not None
            )
        )

    async def fetch_items(self, *args, **kwargs):
        items = await super().fetch_items(*args, **kwargs)

        items_lists = defaultdict(list)
        filtered_list = []
        for item in items:
            items_lists[item.UUID].append(item)
        for items_list in items_lists.values():
            filtered_list.append(max(items_list))

        return filtered_list


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await NtmRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
