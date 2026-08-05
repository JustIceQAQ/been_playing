import asyncio
import secrets
from typing import cast

import bs4
import httpx

from app.museums.nstm.parse import NsTmParse
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import generate_headers
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3


class NsTmRunner(RunnerInit):  # TODO: 壞掉中...
    translation = BeautifulSoupTranslation
    use_parse = NsTmParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.kaohsiung.sanmin_64000050,
            fullname="國立科學工藝博物館",
            code_name="NsTm",
            external_link="https://www.nstm.gov.tw/ExhibitionList.aspx?ExhibitionType=1&Period=1",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="22.64161262350391, 120.32253339088527"),
                raw_coordinates="22.64161262350391, 120.32253339088527",
            ),
            venue_type=VenueType.MUSEUM,
        )

    async def sub_fetch_response(self, client: httpx.AsyncClient, url: str) -> list[str]:
        sub_response = []
        for p_index in range(0, 2, 1):
            response = await client.get(url, params={"Pindex": p_index, "ExhibitionType": "1", "Period": "1"})
            response.raise_for_status()
            if response.is_success:
                sub_response.append(response.text)
            else:
                break
        return sub_response

    async def fetch_response(self):
        semaphore = asyncio.Semaphore(1)
        limits = httpx.Limits(max_connections=5, max_keepalive_connections=2)
        timeout = httpx.Timeout(10.0, connect=5.0)
        headers = generate_headers(
            referer="https://www.nstm.gov.tw/ExhibitionList.aspx?appname=Exhibition",
            need_upgrade_insecure_requests=True,
            other_headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-TW,zh;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Cache-Control": "no-cache",
            },
        )
        cookies = httpx.Cookies()
        cookies.set("ASP.NET_SessionId", secrets.token_hex(16), domain="www.nstm.gov.tw")
        cookies.set("CONSENT", "YES+", domain="www.nstm.gov.tw")
        urls = [
            "https://www.nstm.gov.tw/ExhibitionList.aspx",
            # "https://www.nstm.gov.tw/ExhibitionList.aspx?ExhibitionType=2&Period=1",
        ]
        async with HttpxAsyncClient(
            headers=headers,
            cookies=cookies,
            http2=False,
            limits=limits,
            timeout=timeout,
        ) as client:
            responses = []
            async with semaphore:
                for url in urls:
                    response = await self.sub_fetch_response(client, url)
                    responses.append(response)
            ok = []
            for response in responses:
                ok.extend(response)
        return ok

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        ok_data = []
        for parse in parsed:
            ok_data.extend(parse.select("div.exhi_data_list"))
        return ok_data


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await NsTmRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
