import asyncio

from rnet import Proxy

from app.platform.klook.parse import KLookParse
from configs.settings import get_settings
from helpers.cache import NoneCache
from helpers.crawler.rnet.helper import RNetAsyncClient
from helpers.headers_helper import generate_headers
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.storage.symbol import VenueType
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
    is_sort = False

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
            venue_type=VenueType.PLATFORM,
        )

    async def fetch_response(self):
        responses = []
        headers = generate_headers(
            not_use_user_agent=True,
            other_headers={
                "accept": "text/html,application/xhtml+xml,application/xml;"
                "q=0.9,image/avif,image/webp,image/apng,*/*;"
                "q=0.8,application/signed-exchange;"
                "v=b3;"
                "q=0.7",
                "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            },
        )
        runtime_settings = get_settings()
        proxies = None if runtime_settings.PROXY_POOL is None else [Proxy.all(runtime_settings.PROXY_POOL)]
        async with RNetAsyncClient(
            proxies=proxies,
        ) as client:
            response = await client.get(self.target_url.format(page_num=1), headers=headers)
            if not response.status_code.is_success():
                return responses
            content = await response.json()
            responses.append(content)
            page_size = int(content.get("result").get("page_size"))
            total = int(content.get("result").get("total"))
            for page in range(2, total // page_size + 2):
                sub_response = await client.get(self.target_url.format(page_num=page), headers=headers)
                if not sub_response.status_code.is_success():
                    return responses
                content = await sub_response.json()
                responses.append(content)
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
