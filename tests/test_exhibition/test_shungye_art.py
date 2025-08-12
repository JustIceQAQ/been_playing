import uuid

import httpx
import pytest
from bs4 import BeautifulSoup

from helpers.headers_helper import UA


@pytest.mark.asyncio
async def test_shungye_art_url():
    url = "https://www.shungye-art.org/show_now.php"
    headers = {"user-agent": UA.random, "referer": url}
    cookies = {
        "CONSENT": "YES+",
        "PHPSESSID": uuid.uuid4().hex,
    }
    async with httpx.AsyncClient(
        timeout=None, headers=headers, cookies=cookies
    ) as client:
        response = await client.get(url)
        response.raise_for_status()
    with open("shungye-art.html", "b+w") as f:
        f.write(response.content)


def test_pased_shungye_art_html():
    with open("shungye-art.html", "rb+") as f:
        context = f.read()
    soup = BeautifulSoup(context, "html.parser")
    now = soup.find("a", {"id": "Now"}).next_element.next_element.select(".indexnews1")
    notice = soup.find("a", {"id": "Notice"}).next_element.next_element.select(
        ".indexnews1"
    )
    now_ex = now + notice
    print()
    for ex in now_ex:
        title = ex.select_one("div.fig > h4").text.strip()
        source = (
            "https://www.shungye-art.org/" + ex.find("a").attrs["href"].split("&")[0]
        )
        fig = (
            "https://www.shungye-art.org/"
            + ex.select_one("a > div.info2")
            .get("style")
            .split("background: url(")[1]
            .split(");")[0]
        )
        date = ex.select_one("div.fig > p").text.strip()

        print(title, date, fig, source)
