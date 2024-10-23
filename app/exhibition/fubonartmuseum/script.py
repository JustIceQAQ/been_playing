import bs4
import httpx

from app.exhibition.fubonartmuseum.parse import FuBonArtMuseumParse
from helpers.headers_helper import get_header
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import Information
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
            fullname="富邦美術館",
            code_name="FuBonArtMuseum",
            external_link="https://www.fubonartmuseum.org/Default",
        )

    async def fetch_response(self):
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.get(
                "https://www.fubonartmuseum.org/Default", headers=get_header()
            )
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select(
            "div#homepage-swiper-exhibitions > div.swiper-wrapper > div"
        )


if __name__ == "__main__":
    FuBonArtMuseumRunner().run()
