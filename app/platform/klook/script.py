import asyncio
import json

from app.platform.klook.parse import KLookParse
from configs.settings import get_settings
from helpers.cache.none.helper import NoneCache
from helpers.crawler.scraper.helper import ScraperAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class KLookRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = KLookParse
    target_url = (
        "https://www.klook.com/v1/enteventapisrv/public/content/query_v3?"
        "k_lang=zh_TW"
        "&k_currency=TWD"
        "&area=city_19"
        "&page_size=24"
        "&page_num={page_num}"
        "&filters=convention_exhibition"
        "&sort=latest"
        "&date=next_30_days"
        "&start_date="
        "&end_date="
        "&keywords="
    )

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="KLook 客路",
            code_name="KLook",
            external_link="https://www.klook.com/zh-TW/event/search/listing/?"
            "area=city_19"
            "&filters=convention_exhibition"
            "&date=next_30_days"
            "&sort=latest"
            "&page=1",
        )

    async def fetch_response(self):
        responses = []
        headers = {
            **get_header(),
            "accept": "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,image/apng,*/*;"
            "q=0.8,application/signed-exchange;"
            "v=b3;"
            "q=0.7",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        runtime_settings = get_settings()
        async with ScraperAsyncClient(
            api_key=runtime_settings.SCRAPER_API_KEY
        ) as client:
            response = await client.get(
                self.target_url.format(page_num=1), headers=headers
            )
            if response.status_code != 200:
                return responses
            content = response.response.body.get("content", None)
            if content is None:
                response_json = response.response.body
            else:
                response_json = json.loads(
                    BeautifulSoupTranslation()
                    .translation_to_object(response.response.body.get("content"))
                    .find("pre")
                    .get_text()
                )
            responses.append(response_json)
            page_size = int(response_json.get("result").get("page_size"))
            total = int(response_json.get("result").get("total"))
            for page in range(2, total // page_size + 2):
                sub_response = await client.get(
                    self.target_url.format(page_num=page), headers=headers
                )
                if sub_response.status_code != 200:
                    return responses
                responses.append(sub_response.response.body)
        return responses

    async def fetch_parsed(self):
        items = []
        parsers: list[dict] = await super().fetch_parsed()
        for parsed in parsers:
            items.extend(parsed.get("result").get("data_list"))
        return items


async def main():
    await KLookRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
