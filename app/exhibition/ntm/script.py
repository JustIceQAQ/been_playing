import asyncio
from collections import defaultdict
from itertools import chain

import bs4

from app.exhibition.ntm.parse import NtmParse, PathQuery
from helpers.cache.none.helper import NoneCache
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
        )

    async def fetch_response(self):
        headers = get_header()
        urls_template = "https://www.ntm.gov.tw/News_actives.aspx?n={n}&sms={sms}&page=1&PageSize=50"
        path_query_datas: list[PathQuery] = [
            PathQuery(n=5472, sms=13389),
            PathQuery(n=5473, sms=13389),
            PathQuery(n=5474, sms=13389),
            PathQuery(n=5478, sms=13389),
            PathQuery(n=5477, sms=13389),
        ]
        async with HttpxAsyncClient(headers=headers) as client:
            tasks = [
                client.get(
                    urls_template.format(n=path_query_data.n, sms=path_query_data.sms)
                )
                for path_query_data in path_query_datas
            ]

            responses = await asyncio.gather(*tasks)

        return [response.text for response in responses]

    async def fetch_parsed(self) -> list:
        parsers: list[bs4.BeautifulSoup] = await super().fetch_parsed()
        return list(
            chain.from_iterable(
                parser.select_one("#CCMS_Content").select(
                    "ul[data-child] > li[data-index] > div.area-essay"
                )
                for parser in parsers
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
