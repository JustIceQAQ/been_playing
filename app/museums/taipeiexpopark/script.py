import asyncio
import datetime
from typing import cast

import bs4

from app.museums.taipeiexpopark.parse import TaipeiExPoParkParse
from helpers.crawler.headers_helper import generate_cookies, generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.coordinate import Coordinate, GeoPoint
from helpers.storage.helper import Information
from helpers.symbol.taiwan import Taiwan
from helpers.symbol.venue import VenueType
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import get_date, month_3, to_roc_era_year


class TaipeiExPoParkRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = TaipeiExPoParkParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            location_code=Taiwan.taipei.zhongshan_63000040,
            fullname="花博公園",
            code_name="TaipeiExPoPark",
            external_link="https://www.expopark.taipei/News_Exhibition.aspx?n=247&sms=9029",
            branch_coordinates=Coordinate(
                geo_point=GeoPoint(raw_coordinates="25.069720986746507, 121.52071496978188"),
                raw_coordinates="25.069720986746507, 121.52071496978188",
            ),
            venue_type=VenueType.CREATIVE_PARK,
        )

    async def fetch_response(self):
        headers = generate_headers(
            origin="https://www.expopark.taipei",
            referer="https://www.expopark.taipei/News_Exhibition.aspx?n=247&sms=9029",
        )
        cookies = generate_cookies(
            need_asp_net_session_id=True,
            other_cookies={
                "font-size-": "medium",
                "NewsCatergoryLevel1_247": "undefined",
                "NewsCatergoryLevel2_247": "undefined",
            },
        )
        params = {
            "n": 247,
            "sms": 9029,
            "PageSize": 50,
            "page": 1,
            "Create": 1,
        }
        this_start_date = get_date.now
        this_start_date_format = this_start_date.strftime("%Y/%m/%d")
        this_start_date_format = this_start_date_format.replace(
            str(this_start_date.year), str(to_roc_era_year(this_start_date.year))
        )

        this_end_date = this_start_date + datetime.timedelta(days=90)
        this_end_date_format = this_end_date.strftime("%Y/%m/%d")
        this_end_date_format = this_end_date_format.replace(
            str(this_end_date.year), str(to_roc_era_year(this_end_date.year))
        )

        data = {
            "jNewsModule_field_SDate4": this_start_date_format,
            "jNewsModule_field_EDate4": this_end_date_format,
            "jNewsModule_BtnSend": "送出查詢",
        }
        async with HttpxAsyncClient(headers=headers) as client:
            pre_response = await client.get("https://www.expopark.taipei/News_Exhibition.aspx?n=247&sms=9029")
            pre_response.raise_for_status()
            pre_response_parsed = self.translation().translation_to_object(pre_response.text)
            view_state = pre_response_parsed.select_one("#__VIEWSTATE").attrs.get("value")
            view_state_generator = pre_response_parsed.select_one("#__VIEWSTATEGENERATOR").attrs.get("value")
            data["__VIEWSTATE"] = view_state
            data["__VIEWSTATEGENERATOR"] = view_state_generator

            response = await client.post(
                "https://www.expopark.taipei/News_Exhibition.aspx",
                params=params,
                data=data,
                cookies=cookies,
            )
            response.raise_for_status()
            posted_url = response.url
            csn = [25, 41, 43]
            sub_responses = await asyncio.gather(
                *[
                    client.get(posted_url.copy_merge_params({"_CSN": str(c)}), headers=headers, cookies=cookies)
                    for c in csn
                ]
            )
            responses = [sub_response.text for sub_response in sub_responses]
        return responses

    async def fetch_parsed(self):
        parsed = cast(list[bs4.BeautifulSoup], await super().fetch_parsed())
        p = []
        for row in parsed:
            p.extend(row.select_one("div.page-block").select("div.event-list"))
        return p


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await TaipeiExPoParkRunner().run(none_cache, none_image_hosting, develop_mode=True)


if __name__ == "__main__":
    asyncio.run(main())
