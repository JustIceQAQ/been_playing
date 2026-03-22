import httpx
import pytest
from bs4 import BeautifulSoup

from helpers.headers_helper import generate_headers


@pytest.mark.asyncio
async def test_ceramics():
    headers = generate_headers(
        x_requested_with="XMLHttpRequest",
        referer="https://www.ceramics.ntpc.gov.tw/xmdoc?xsmsid=0J148497613881029302",
        origin="https://www.ceramics.ntpc.gov.tw",
        host="www.ceramics.ntpc.gov.tw",
    )
    async with httpx.AsyncClient(timeout=None, headers=headers, follow_redirects=True) as client:
        html_response = await client.get("https://www.ceramics.ntpc.gov.tw/xmdoc?xsmsid=0J148497613881029302")
        soup = BeautifulSoup(html_response.text, "html5lib")
        request_verification_token = soup.find("input", {"name": "__RequestVerificationToken"})["value"]
        xsms_id = soup.find("input", {"name": "XsmSId"})["value"]
        condss_id = soup.find("input", {"name": "CondsSId"})["value"]

        data = {
            "__RequestVerificationToken": request_verification_token,
            "XsmSId": xsms_id,
            "CondsSId": condss_id,
            "ExecAction": "Q",
            "IndexOfPages": 1,
            "PageSize": 50,
        }
        xmdoc_response = await client.post("https://www.ceramics.ntpc.gov.tw/xmdoc/indexaction", data=data)
        xmdoc_soup = BeautifulSoup(xmdoc_response.text, "html5lib")
        print(xmdoc_soup)
