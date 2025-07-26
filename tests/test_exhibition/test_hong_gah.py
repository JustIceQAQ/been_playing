import datetime
import urllib.parse
import httpx
import pytest
from bs4 import BeautifulSoup

from helpers.headers_helper import UA


@pytest.mark.asyncio
async def test_hong_gah_url():
    headers = {
        "user-agent": UA.random,
        "x-requested-with": "XMLHttpRequest",
        "referer": "https://hong-gah.org.tw/exhibitions-zh",
        "host": "hong-gah.org.tw",
    }

    url = "https://hong-gah.org.tw/exhibitions-zh/page/1"
    async with httpx.AsyncClient(
        timeout=None, headers=headers, follow_redirects=True
    ) as client:
        response = await client.get(url)
        response.raise_for_status()
    soup = BeautifulSoup(response.text, "html5lib")
    with open("hong_gah_demo.html", "w", encoding="utf-8") as f:
        f.write(str(soup))


def test_hong_gah_format():
    print()
    with open("hong_gah_demo.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html5lib")
    project = soup.find("div", {"class": "portfolio-grid"})
    items = project.find_all("div", {"class": "ohio-project-item"})

    for item in items:
        source_url = item.find("a", {"class": "card-image"})["href"]
        img_element = item.find("img")
        image_url = urllib.parse.quote(img_element.attrs["src"], safe=":/")
        title = img_element["alt"]

        heading = item.find("div", {"class": "heading"})
        raw_date = heading.next_element.next_element.next_element.next_element.get_text().strip()
        date_range = format_date_ranges(raw_date)
        print(title, image_url, date_range, source_url)


def format_date_ranges(raw_text: str) -> str | None:
    result = None
    for line in raw_text.strip().splitlines():
        if not line.strip():
            continue
        start_str, end_str = line.split("-")

        if len(end_str) == 5:
            start_year = start_str.split(".")[0]
            end_str = f"{start_year}.{end_str}"
        elif len(end_str) == 10 and end_str.count(".") == 2:
            pass
        else:
            start_year = start_str.split(".")[0]
            if "." in end_str:
                end_str = f"{start_year}.{end_str}"
            else:
                raise ValueError(f"無法解析的日期格式: {line}")
        start_date = datetime.datetime.strptime(start_str, "%Y.%m.%d").strftime(
            "%Y-%m-%d"
        )
        end_date = datetime.datetime.strptime(end_str, "%Y.%m.%d").strftime("%Y-%m-%d")
        result = f"{start_date} ~ {end_date}"
    return result
