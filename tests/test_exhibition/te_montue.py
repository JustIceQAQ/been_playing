import pytest
from bs4 import BeautifulSoup
import httpx

from helpers.headers_helper import UA


@pytest.mark.asyncio
async def test_motue():
    headers = {"user-agent": UA.random}
    async with httpx.AsyncClient(headers=headers, timeout=None) as client:
        url = "https://montue.ntue.edu.tw/exhibitions-upcoming/"
        response = await client.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        divs = soup.find_all(
            "div",
            {"class": "ptsc pt-sc sc-slider exhibition-slider hide-title hide-mobile"},
        )
        for div in divs:
            print(div.find("a").get("href"))
