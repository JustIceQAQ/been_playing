import secrets

import httpx
import pytest
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

UA = UserAgent(browsers="chrome", os=["windows", "macos"], platforms="pc")


@pytest.mark.asyncio
async def test_base():
    url = "https://www.ocam.org.tw/tw/Exhibition/NowPage"
    headers = {
        "host": "www.ocam.org.tw",
        "user-agent": UA.random,
        "origin": "https://www.ocam.org.tw",
        "referer": "https://www.ocam.org.tw/tw/Exhibition/OCAM",
        "x-requested-with": "XMLHttpRequest",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "priority": "u=1, i",
    }
    cookies = {"CONSENT": "YES+", "PHPSESSID": secrets.token_hex(16)}
    data = {"site": "OCAM", "nowpage": 1, "ispast": 0}
    async with httpx.AsyncClient(
        timeout=None, headers=headers, cookies=cookies
    ) as client:
        response = await client.post(url, data=data)
        response.raise_for_status()
    soup = BeautifulSoup(response.content, "html5lib")
    items = soup.select("figcaption")
    for item in items:
        print(item.parent)
