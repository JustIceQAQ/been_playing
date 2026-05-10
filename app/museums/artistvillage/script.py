import asyncio
from typing import cast

from app.museums.artistvillage.parse import ArtistVillageParse
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.symbol.venue import VenueType
from helpers.symbol.taiwan import Taiwan
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3, get_this_date_year


class ArtistVillageRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = ArtistVillageParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.zhongzheng_63000050,
            fullname="寶藏巖國際藝術村",
            code_name="ArtistVillage",
            external_link="https://www.artistvillage.org/event.php",
            branch_coordinates=Coordinate(
                raw_coordinates="25.011242493165764, 121.53225091835029",
            ),
            venue_type=VenueType.ART_VILLAGE,
        )

    async def fetch_response(self):
        headers = generate_headers() | {
            "x-requested-with": "XMLHttpRequest",
            "referer": "https://www.artistvillage.org/event.php",
            "origin": "https://www.artistvillage.org",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        cookies = generate_cookies(need_phpsessid=True)
        next_year = get_this_date_year() + 1
        data = {
            "post_type": "event",
            "start_date": "20251030",  # date_format_digit(),
            "end_date": f"{next_year}1231",
            "method": "get_posts_list_month",
        }
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.post("https://www.artistvillage.org/ajax.php", data=data, cookies=cookies)
        return response.json()

    async def fetch_parsed(self):
        parsed = cast(list[dict], await super().fetch_parsed())
        return parsed


async def main():
    from helpers.cache.none.helper import NoneCache
    from helpers.image.none.helper import NoneImage

    await ArtistVillageRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
