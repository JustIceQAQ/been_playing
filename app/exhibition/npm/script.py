import asyncio

import bs4

from app.exhibition.npm.parse import NpmColParse, NpmRowParse, NpmPreviewParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import ExhibitionItem, Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_6


class NpmRunner(RunnerInit):
    translation = BeautifulSoupTranslation

    def set_cache_expire(self) -> int | None:
        return month_6()

    def set_information(self) -> "Information":
        return Information(
            fullname="國立故宮博物院",
            code_name="Npm",
            external_link="https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1&type=1",
        )

    async def fetch_response(self):
        # runtime_setting = get_settings()
        this_header = {
            "referer": "https://www.npm.gov.tw/",
            "upgrade-insecure-requests": "1",
            "host": "www.npm.gov.tw",
        }
        async with HttpxAsyncClient() as client:
            results = await asyncio.gather(
                *[
                    client.get(
                        "https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1&type=1",
                        headers={**get_header(), **this_header},
                    ),
                    client.get(
                        "https://www.npm.gov.tw/Exhibition-Preview.aspx?sno=03000061&l=1",
                        headers={**get_header(), **this_header},
                    ),
                ]
            )
        # async with ScrapeDoAsyncClient(
        #     api_key=runtime_setting.SCRAPE_DO_API_KEY
        # ) as client:
        #     results = await asyncio.gather(
        #         *[
        #             client.get(
        #                 "https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1&type=1",
        #                 headers={**get_header(), **this_header},
        #             ),
        #             client.get(
        #                 "https://www.npm.gov.tw/Exhibition-Preview.aspx?sno=03000061&l=1",
        #                 headers={**get_header(), **this_header},
        #             ),
        #         ]
        #     )
        for response in results:
            response.raise_for_status()

        return results

    async def fetch_parsed(self) -> dict:
        parsed_dataset: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        parsed, parsed_dataset_1 = parsed_dataset
        if parsed is None and parsed_dataset_1 is None:
            return {}
        parsed_dict = {}
        if parsed is not None:
            datasets_row = parsed.select("ul.mt-4 li.mb-8")
            datasets_col = parsed.select("ul.mt-10 li.mb-8")
            parsed_dict = {"row": datasets_row, "col": datasets_col}

        if parsed_dataset_1 is not None:
            preview_parsed = parsed_dataset_1.select(
                ".navtabs-content-static ul.grid > li.mb-8"
            )
            parsed_dict["preview"] = preview_parsed
        return parsed_dict

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
        if runtime_parsed.get("row", None) is not None:
            exhibition_items.extend(
                self._sub_fetch_items(
                    runtime_parsed["row"],
                    NpmRowParse,
                    target_domain="https://www.npm.gov.tw/",
                )
            )
        if runtime_parsed.get("col", None) is not None:
            exhibition_items.extend(
                self._sub_fetch_items(
                    runtime_parsed["col"],
                    NpmColParse,
                    target_domain="https://www.npm.gov.tw/",
                )
            )
        if runtime_parsed.get("preview", None) is not None:
            exhibition_items.extend(
                self._sub_fetch_items(
                    runtime_parsed["preview"],
                    NpmPreviewParse,
                    target_domain="https://www.npm.gov.tw/",
                )
            )
        return exhibition_items


async def main():
    await NpmRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
