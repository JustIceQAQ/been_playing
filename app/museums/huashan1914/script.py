import asyncio
from typing import cast

import bs4

from app.museums.huashan1914.information import HuaShan1914Information
from app.museums.huashan1914.parse import huashan1914Parse
from app.museums.huashan1914.utils import find_exhibition_list, get_event_category_data, get_event_venue_data
from helpers.crawler.headers_helper import generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.json.helper import DevalueToJsonTranslation, JsonTranslation
from helpers.utils_helper import month_3


class HuaShan1914Runner(RunnerInit):
    translation = JsonTranslation
    use_parse = huashan1914Parse
    temp = {"event_category_data": {}, "event_venue_data": {}}

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return HuaShan1914Information.get_information()

    async def fetch_response(self):
        index = 1
        datasets = []
        async with HttpxAsyncClient(headers=generate_headers()) as client:
            while True:
                response = await client.get(
                    f"https://www.huashan1914.com/exhibition?page={index}",
                )
                parsed = bs4.BeautifulSoup(response.text, "html5lib").find("script", id="__NUXT_DATA__").string
                r = DevalueToJsonTranslation().translation_to_object(parsed)
                dataset = find_exhibition_list(r)
                if dataset:
                    datasets.append(dataset)
                    self.temp["event_category_data"] |= get_event_category_data(r)
                    self.temp["event_venue_data"] |= get_event_venue_data(r)
                    index = index + 1
                else:
                    break
        return datasets

    async def fetch_parsed(self):
        items = []
        parsers = cast(list[dict], await super().fetch_parsed())
        for parsed in parsers:
            items.extend(parsed)
        return items

    async def fetch_items(self, *args, **kwargs):
        return await super().fetch_items(target_domain="https://www.huashan1914.com", **self.temp)


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await HuaShan1914Runner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
