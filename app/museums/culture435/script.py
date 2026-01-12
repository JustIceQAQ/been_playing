import asyncio
import decimal

import bs4
from app.museums.culture435.parse import Culture435Parse
from helpers.headers_helper import get_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3
from helpers.cache.none.helper import NoneCache
from helpers.image.none.helper import NoneImage


class Culture435Runner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = Culture435Parse
    is_sort = False

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.new_taipei_city,
            fullname="板橋435藝文特區",
            code_name="Culture435",
            external_link="https://www.435.culture.ntpc.gov.tw/xmdoc?xsmsid=0G256373177821958325",
            branch_coordinates=Coordinate(raw_coordinates="25.024344268554966, 121.45235225442633"),
        )

    async def fetch_response(self):
        xsmsid = "0G256373177821958325"
        first_url = "https://www.435.culture.ntpc.gov.tw/xmdoc"
        headers = get_headers(host="www.435.culture.ntpc.gov.tw")
        async with HttpxAsyncClient(headers=headers) as client:
            first_response = await client.get(
                first_url, headers=headers, params={"xsmsid": xsmsid}
            )
            first_response.raise_for_status()
            p = BeautifulSoupTranslation().translation_to_object(
                first_response.text,
            )
            conds_s_id = p.find("input", {"id": "CondsSId"}).attrs["value"]
            request_verification_token = p.find(
                "input", {"name": "__RequestVerificationToken"}
            ).attrs["value"]
            url = "https://www.435.culture.ntpc.gov.tw/xmdoc/indexaction"
            headers["x-requested-with"] = "XMLHttpRequest"
            headers[
                "referer"
            ] = "https://www.435.culture.ntpc.gov.tw/xmdoc?xsmsid=0G256373177821958325"
            headers["origin"] = "https://www.435.culture.ntpc.gov.tw"
            headers["host"] = "www.435.culture.ntpc.gov.tw"
            headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            response = await client.post(
                url,
                headers=headers,
                data={
                    "XsmSId": xsmsid,
                    "CondsSid": conds_s_id,
                    "__RequestVerificationToken": request_verification_token,
                    "ExecAction": "Q",
                    "IndexOfPages": "0",
                    "PageSize": 15,
                    "Keyword": "",
                },
                follow_redirects=True,
            )
            response.raise_for_status()
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("div.item")


async def main():
    await Culture435Runner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
