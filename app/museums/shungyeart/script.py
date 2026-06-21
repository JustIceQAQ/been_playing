import asyncio

import bs4
from app.museums.shungyeart.information import ShungYeArtInformation
from app.museums.shungyeart.parse import ShungYeArtParse
from app.museums.shungyeart.social_media import ShungYeArtSocialMedia
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3

from typing import cast


class ShungYeArtRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = ShungYeArtParse
    use_suffix_item_from_file_func = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return ShungYeArtInformation.get_information()

    def set_social_media(self):
        return ShungYeArtSocialMedia.get_social_media()

    async def fetch_response(self):
        url = "https://www.shungye-art.org/show_now.php"
        headers = generate_headers(referer=url)
        cookies = generate_cookies(need_phpsessid=True, need_consent=True)

        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get(url, cookies=cookies)
        return response.text

    async def fetch_parsed(self):
        now_ex = []
        parsed = cast(bs4.BeautifulSoup, await super().fetch_parsed())
        now = parsed.find("a", {"id": "Now"})
        if now is not None:
            now_ex.extend(now.find_all_next(class_="indexnews1"))

        notice = parsed.find("a", {"id": "Notice"}).find_all_next(class_="indexnews1")

        if notice is not None:
            now_ex.extend(notice.find_all_next(class_="indexnews1"))

        return now_ex


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await ShungYeArtRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
