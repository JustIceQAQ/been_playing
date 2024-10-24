import asyncio

import bs4
import httpx

from app.exhibition.cksmh.parse import CKSMHParse
from helpers.cache.disk.helper import DiskCache
from helpers.image.imgur.helper import ImgurImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class CKSMHRunner(RunnerInit):
    """中正紀念堂"""

    translation = BeautifulSoupTranslation
    use_parse = CKSMHParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="中正紀念堂",
            code_name="CKSMH",
            external_link="https://www.cksmh.gov.tw/activitysoonlist_369.html",
        )

    async def fetch_response(self) -> str:
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(
                "https://www.cksmh.gov.tw/News_Actives_photo.aspx?n=6067&sms=14954"
            )
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        div = parsed.select_one("div.group-list.page-block")
        return div.find("ul").find_all("li")


async def main():
    ii = ImgurImage(client_id="8cf25722e8ecbeb")
    dc = DiskCache()

    runner = CKSMHRunner()
    await runner.run(dc, ii)


if __name__ == "__main__":
    asyncio.run(main())
