import asyncio

import bs4

from app.exhibition.npm.parse import NpmColParse, NpmRowParse
from configs.settings import get_settings
from helpers.cache.none.helper import NoneCache
from helpers.crawler.scrape_do.helper import ScrapeDoAsyncClient
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
        runtime_setting = get_settings()
        headers = get_header()

        async with ScrapeDoAsyncClient(
            api_key=runtime_setting.SCRAPE_DO_API_KEY
        ) as client:
            response = await client.get(
                "https://www.npm.gov.tw/Exhibition-Current.aspx?sno=03000060&l=1&type=1",
                headers=headers,
            )
        return response.response.body

    async def fetch_parsed(self) -> dict:
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        datasets_row = parsed.select("ul.mt-4 li.mb-8")
        datasets_col = parsed.select("ul.mt-10 li.mb-8")
        return {"row": datasets_row, "col": datasets_col}

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
                runtime_parsed["row"],
                NpmRowParse,
                target_domain="https://www.npm.gov.tw/",
            )
        )
        exhibition_items.extend(
            self._sub_fetch_items(
                runtime_parsed["col"],
                NpmColParse,
                target_domain="https://www.npm.gov.tw/",
            )
        )
        return exhibition_items


async def main():
    await NpmRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
