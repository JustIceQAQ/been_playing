import bs4

from app.museums.fubonartmuseum.parse import FuBonArtMuseumParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information, Coordinate
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class FuBonArtMuseumRunner(RunnerInit):
    """富邦美術館"""

    translation = BeautifulSoupTranslation
    use_parse = FuBonArtMuseumParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=TaiwanCity.taipei_city,
            fullname="富邦美術館",
            code_name="FuBonArtMuseum",
            external_link="https://www.fubonartmuseum.org/Default",
            branch_coordinates=Coordinate(raw_coordinates="25.039545226356974, 121.57119466791848"),
            venue_type=VenueType.MUSEUM,
        )

    async def fetch_response(self):
        async with HttpxAsyncClient(headers=generate_headers()) as client:
            response = await client.get(
                "https://www.fubonartmuseum.org/Default",
            )
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("div#homepage-swiper-exhibitions > div.swiper-wrapper > div")


if __name__ == "__main__":
    FuBonArtMuseumRunner().run()
