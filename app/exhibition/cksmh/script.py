import asyncio

import bs4

from app.exhibition.cksmh.parse import CKSMHParse
from helpers.cache import DiskCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
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
            map_url=(
                "https://www.google.com/maps/embed?"
                "pb=!1m18!1m12!1m3!1d7229.964450035861!"
                "2d121.51870450237908!3d25.034677281972296!"
                "2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!"
                "1m2!1s0x3442a99db9a2a94d%3A0x43e9034292df69b2!2z5ZyL56uL5Lit5q2j57SA5b-"
                "15aCC!5e0!3m2!1szh-TW!2stw!4v1739199635272!5m2!1szh-TW!2stw"
            ),
        )

    async def fetch_response(self) -> str:
        async with HttpxAsyncClient() as client:
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
