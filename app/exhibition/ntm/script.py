import asyncio
from collections import defaultdict
from itertools import chain

import bs4

from app.exhibition.ntm.parse import NtmParse, all_branch
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class NtmRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = NtmParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="國立臺灣博物館",
            code_name="Ntm",
            external_link="https://www.ntm.gov.tw/submenu_178.html",
            address="臺北市中正區襄陽路2號",
            google_map_place_id="ChIJcRV3WHOpQjQRFpgzTpxZWgo",
        )

    async def fetch_response(self):
        headers = get_header()
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
        parsers: list[bs4.BeautifulSoup] = await super().fetch_parsed()
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
    await NtmRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
