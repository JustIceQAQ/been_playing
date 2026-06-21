import asyncio
from typing import cast

from wreq import Proxy

from app.platform.klook.parse import KLookParse
from configs.settings import get_settings
from helpers.crawler.wreq.helper import WReqAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.symbol.venue import VenueType
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3


class KLookRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = KLookParse
    target_url = (
        "https://www.klook.com/v1/enteventapisrv/public/content/query_v3?"
        "k_lang=zh_TW"
        "&k_currency=TWD"
        "&area=coureg_1014"
        "&page_size=23"
        "&page_num={page_num}"
        "&filters=convention_exhibition"
        "&sort=coming_end"
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
            external_link=self.target_url.format(page_num=1),
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
        async with WReqAsyncClient(
            proxies=proxies,
        ) as client:
            response = await client.get(self.target_url.format(page_num=1), headers=headers)
            if not response.status.is_success():
                return responses
            content = await response.json()
            responses.append(content)
            page_size = int(content.get("result").get("page_size"))
            total = int(content.get("result").get("total"))
            for page in range(2, total // page_size + 2):
                sub_response = await client.get(self.target_url.format(page_num=page), headers=headers)
                if not sub_response.status.is_success():
                    return responses
                content = await sub_response.json()
                responses.append(content)
        return responses

    async def fetch_parsed(self):
        items = []
        parsers = cast(list[dict], await super().fetch_parsed())
        for parsed in parsers:
            result = parsed.get("result")
            if result is None:
                continue
            data_list = result.get("data_list")
            if data_list is None:
                continue
            items.extend(data_list)
        return items


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await KLookRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
