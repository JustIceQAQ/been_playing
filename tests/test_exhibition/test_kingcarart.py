import asyncio
import http

import httpx
import pytest
from bs4 import BeautifulSoup, Tag

from helper.header_helper import UA


def get_items(obj: BeautifulSoup) -> list[Tag]:
    return obj.select("ul.ex-list-box > li")


@pytest.mark.asyncio
async def test_kingcarart():
    url = "https://www.kingcarart.org.tw/exhibitions/current?nanjing=true&chengde=true&yuanshan=true&page={page}"
    headers = {"user-agent": UA.random}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(url.format(page=1))
        parsed = BeautifulSoup(response.text, "html5lib")
        get_page_number = len(parsed.select("div.pagin-box > div.page-link"))

        items = []
        items.extend(get_items(parsed))

        tasks = [
            client.get(url.format(page=page_flag))
            for page_flag in range(2, get_page_number + 1)
        ]

        tasks_result = await asyncio.gather(*tasks)

        for task_result in tasks_result:
            sub_parsed = BeautifulSoup(task_result.text, "html5lib")
            items.extend(get_items(sub_parsed))

        assert response.status_code == http.HTTPStatus.OK
