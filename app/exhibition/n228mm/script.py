import asyncio
import json

import bs4
from app.exhibition.n228mm.parse import N228MMParse
from app.exhibition.n228mm.schemas import CommonConfig, query_p
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class N228MMRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = N228MMParse
    is_sort = False
    is_unique = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="二二八國家紀念館",
            code_name="n228mm",
            external_link="https://www.228.org.tw/exhibitionsnew",
        )

    async def fetch_response(self):
        headers = dict(**get_header())
        async with HttpxAsyncClient() as client:
            response_1 = await client.get(
                "https://www.228.org.tw/exhibitionsnew", headers=headers
            )
            parsed = bs4.BeautifulSoup(response_1.text, "html5lib")
            wix_viewer_model = parsed.select_one("#wix-viewer-model").string
            wix_viewer_model_dict = json.loads(wix_viewer_model)
            runtime_headers = wix_viewer_model_dict["siteFeaturesConfigs"][
                "dynamicPages"
            ]["prefixToRouterFetchData"]["exhibitionse"]["optionsData"]["headers"]
            x_wix_grid_app_id = runtime_headers["x-wix-grid-app-id"]
            common_config = CommonConfig(BSI=x_wix_grid_app_id).to_query()
            r_query = query_p(x_wix_grid_app_id)
            headers = headers | {
                "referer": "https://www.228.org.tw/",
                "authorization": runtime_headers["Authorization"],
                "commonconfig": common_config,
            }
            response = await client.get(
                "https://www.228.org.tw/_api/cloud-data/v2/items/query",
                headers=headers,
                params={".r": r_query},
            )
        result = response.json()

        return [item["data"] for item in result["dataItems"]]

    async def fetch_parsed(self):
        parsed: list[dict] = await super().fetch_parsed()
        return parsed


async def main():
    await N228MMRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
