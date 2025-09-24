import httpx
import pytest
from bs4 import BeautifulSoup

from helpers.headers_helper import get_header


async def get_response(client: httpx.AsyncClient, url: str) -> str:
    response = await client.get(url)
    response.raise_for_status()
    return response.text


@pytest.mark.asyncio
async def test_khm_html():
    dataset = []
    current_exhibitions_url = "https://khm.org.tw/tw/exhibition/currentexhibitions"
    permanent_exhibitions = "https://khm.org.tw/tw/exhibition/permanentexhibitions"
    headers = {**get_header(), "referer": current_exhibitions_url}
    async with httpx.AsyncClient(headers=headers) as client:
        current_exhibitions_response = await get_response(
            client, current_exhibitions_url
        )
        permanent_exhibitions = await get_response(client, permanent_exhibitions)
    for response_text in (current_exhibitions_response, permanent_exhibitions):
        soup = BeautifulSoup(response_text, "html5lib")
        datas = soup.select("div.exhibition-list div.list-item")
        dataset.extend(datas)
    print(dataset)
