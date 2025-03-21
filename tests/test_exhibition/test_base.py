import httpx
import pytest
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

UA = UserAgent(browsers="chrome", os=["windows", "macos"], platforms="pc")


@pytest.mark.asyncio
async def test_base():
    url = "https://www.artmuse.ntnu.edu.tw/index.php/current_exhibit/"
    headers = {
        "host": "www.artmuse.ntnu.edu.tw",
        "user-agent": UA.random,
    }
    async with httpx.AsyncClient(timeout=None, headers=headers) as client:
        response = await client.get(url)
        response.raise_for_status()
    soup = BeautifulSoup(response.content, "html5lib")
    items = soup.select("figcaption")
    for item in items:
        print(item.parent)
