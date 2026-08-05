import asyncio
from typing import cast

from app.museums.artistvillage.parse import ArtistVillageParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers, generate_cookies
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate
from helpers.storage.helper import ExhibitionItem, Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.translation.json import JsonTranslation
from helpers.utils_helper import month_3, get_date


class ArtistVillageRunner(RunnerInit):
    translation = JsonTranslation
    use_parse = ArtistVillageParse
    use_suffix_item_from_url_auto = True

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
        headers = generate_headers(
            x_requested_with="XMLHttpRequest",
            referer="https://www.artistvillage.org/event.php",
            origin="https://www.artistvillage.org",
        )
        cookies = generate_cookies(need_phpsessid=True)
        next_year = get_date.now_year + 1
        data = {
            "post_type": "event",
            "end_date": f"{next_year}1231",
            "method": "get_posts_list_month",
        }
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.post("https://www.artistvillage.org/ajax.php", data=data, cookies=cookies)
        return response.json()

    async def fetch_parsed(self):
        parsed = cast(list[dict], await super().fetch_parsed())
        return parsed

    async def _get_item_data(self, client, item: ExhibitionItem):
        has_address_cache = await self.cache.aget(f"{item.UUID}-address")
        has_figure_cache = await self.cache.aget(f"{item.UUID}-figure")
        if has_address_cache and has_figure_cache:
            item.address = has_address_cache
            item.figure = has_figure_cache
            return

        response = await client.get(item.source_url)
        soup = BeautifulSoupTranslation().translation_to_object(response.text)
        if soup is None:
            return None
        exhibition_address = None
        exhibition_figure = None
        a_elements = soup.select("div.date p")
        if a_elements:
            for a_element in a_elements:
                value = a_element.get_text(strip=True)
                if "活動地點：" in value:
                    exhibition_address = value.replace("活動地點：", "").strip()
                    break

        og_image = soup.select_one("meta[property='og:image']")
        if og_image:
            exhibition_figure = og_image.attrs.get("content")

        await self.cache.aset(f"{item.UUID}-address", exhibition_address, month_3())
        await self.cache.aset(f"{item.UUID}-figure", exhibition_figure, month_3())

        item.address = exhibition_address
        item.figure = exhibition_figure

    async def suffix_item_from_url_auto(self, items: list[ExhibitionItem]):
        headers = generate_headers()
        async with HttpxAsyncClient(headers=headers) as client:
            tasks = [self._get_item_data(client, item) for item in items]
            await asyncio.gather(*tasks)


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await ArtistVillageRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
