import asyncio
from typing import cast

from app.museums.npm.parse import (
    NpmColParse,
    NpmRowParse,
    NpmPreviewParse,
    SouthNpmParse,
)
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import ExhibitionItem, Information, Coordinate
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_6


class NpmRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    is_sort = False
    output_ics = True
    output_rss = True

    def set_cache_expire(self) -> int | None:
        return month_6()

    def set_information(self) -> "Information":
        return Information(
            fullname="國立故宮博物院",
            code_name="Npm",
            external_link="https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1&type=1",
            raw_coordinates="25.10255940335793, 121.5485139544282",
            branch_coordinates=[
                Coordinate(
                    name="北部院區",
                    location_code=Taiwan.taipei.shilin_63000110,
                    raw_coordinates="25.10255940335793, 121.5485139544282",
                ),
                Coordinate(
                    name="南部院區",
                    location_code=Taiwan.chiayi_county.taibao_10010010,
                    raw_coordinates="23.473459041101574, 120.2928023651772",
                ),
            ],
            venue_type=VenueType.MEMORIAL,
        )

    async def fetch_south_response(self):
        this_header = generate_headers(
            referer="https://south.npm.gov.tw/ExhibitionsListC003110.aspx?appname=Exhibition3112",
            need_upgrade_insecure_requests=True,
            host="south.npm.gov.tw",
        )
        async with HttpxAsyncClient(headers=this_header) as client:
            results = await asyncio.gather(
                *[
                    client.get(
                        "https://south.npm.gov.tw/ExhibitionsListC003110.aspx?appname=Exhibition3112",
                    ),
                    client.get(
                        "https://south.npm.gov.tw/ExhibitionsListC003110.aspx?appname=Exhibition3111",
                    ),
                ]
            )
        for response in results:
            response.raise_for_status()

        return results

    async def fetch_north_response(self):
        this_header = generate_headers(
            referer="https://www.npm.gov.tw/",
            need_upgrade_insecure_requests=True,
            host="www.npm.gov.tw",
        )
        async with HttpxAsyncClient(headers=this_header) as client:
            results = await asyncio.gather(
                *[
                    client.get(
                        "https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1&type=1",
                    ),
                    client.get(
                        "https://www.npm.gov.tw/Exhibition-Preview.aspx?sno=03000061&l=1",
                    ),
                ]
            )
        for response in results:
            response.raise_for_status()

        return results

    async def fetch_response(self):
        north_response = await self.fetch_north_response()
        south_response = await self.fetch_south_response()
        return {
            "north": north_response,
            "south": south_response,
        }

    def fetch_north_parsed(self, dataset: list) -> dict:
        north_parsed, north_parsed_dataset_1 = dataset
        if north_parsed is None and north_parsed_dataset_1 is None:
            return {}
        north_parsed_dict = {}
        if north_parsed is not None:
            datasets_row = north_parsed.select("ul.mt-4 li.mb-8")
            datasets_col = north_parsed.select("ul.mt-10 li.mb-8")
            north_parsed_dict = {"row": datasets_row, "col": datasets_col}

        if north_parsed_dataset_1 is not None:
            preview_parsed = north_parsed_dataset_1.select(".navtabs-content-static ul.grid > li.mb-8")
            north_parsed_dict["preview"] = preview_parsed
        return north_parsed_dict

    def fetch_south_parsed(self, dataset: list) -> list:
        south_parsed, south_parsed_dataset_1 = dataset
        if south_parsed is None and south_parsed_dataset_1 is None:
            return []
        south_parsed_list = []
        if south_parsed is not None:
            datasets_row = south_parsed.select("div.card_wrap > div.kf_imglist")
            south_parsed_list.extend(datasets_row)
        if south_parsed_dataset_1 is not None:
            datasets_row = south_parsed.select("div.card_wrap > div.kf_imglist")
            south_parsed_list.extend(datasets_row)

        return south_parsed_list

    async def fetch_parsed(self) -> dict:
        parsed_dataset = cast(dict[str, list], await super().fetch_parsed())
        north_parsed_dict = self.fetch_north_parsed(parsed_dataset["north"])
        south_parsed_list = self.fetch_south_parsed(parsed_dataset["south"])

        return {
            "north": north_parsed_dict,
            "south": south_parsed_list,
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
        runtime_parsed = cast(dict, self.parsed_)
        if (north := runtime_parsed.get("north")) is not None:
            if (north_row := north.get("row", None)) is not None:
                exhibition_items.extend(
                    self._sub_fetch_items(
                        north_row,
                        NpmRowParse,
                        target_domain="https://www.npm.gov.tw/",
                    )
                )
            if (north_col := north.get("col")) is not None:
                exhibition_items.extend(
                    self._sub_fetch_items(
                        north_col,
                        NpmColParse,
                        target_domain="https://www.npm.gov.tw/",
                    )
                )
            if (north_preview := north.get("preview")) is not None:
                exhibition_items.extend(
                    self._sub_fetch_items(
                        north_preview,
                        NpmPreviewParse,
                        target_domain="https://www.npm.gov.tw/",
                    )
                )

        if (south := runtime_parsed.get("south")) is not None:
            for item in south:
                exhibition_items.append(SouthNpmParse(item).parse_to_base_model(ExhibitionItem, *args, **kwargs))
        return exhibition_items


async def main():
    await NpmRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
