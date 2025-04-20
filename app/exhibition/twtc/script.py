import asyncio
import datetime

import httpx

from app.exhibition.twtc.parse import TwTcParse
from app.exhibition.twtc.schemas import TwTcResponse
from app.exhibition.twtc.utils import get_next_element
from helpers.cache.none import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import ExhibitionItem, Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import date_now, month_3


class TwTcRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = TwTcParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="台北世貿中心",
            code_name="TwTc",
            external_link="https://twtc.com.tw/exhibition?p=home",
        )

    def extract_import(self, response: httpx.Response) -> dict:
        parsed = self.translation().translation_to_object(response.text)
        view_state = parsed.find("input", attrs={"name": "__VIEWSTATE"})["value"]
        view_state_generator = parsed.find(
            "input", attrs={"name": "__EVENTVALIDATION"}
        )["value"]
        event_validation = parsed.find("input", attrs={"name": "__EVENTVALIDATION"})[
            "value"
        ]
        selected_year = parsed.find("select", attrs={"id": "body_ddlYear"}).find(
            "option", {"selected": "selected"}
        )["value"]
        selected_month = parsed.find("select", attrs={"id": "body_ddlMoth"}).find(
            "option", {"selected": "selected"}
        )["value"]
        return {
            "__VIEWSTATE": view_state,
            "__VIEWSTATEGENERATOR": view_state_generator,
            "__EVENTVALIDATION": event_validation,
            "ctl00$body$ddlYear": selected_year,
            "ctl00$body$ddlMoth": selected_month,
        }

    async def fetch_response(self):
        headers = {
            **get_header(),
            "Host": "twtc.com.tw",
            "Pragma": "no-cache",
            "Referer": "https://twtc.com.tw/exhibition?p=home",
        }
        responses = []
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://twtc.com.tw/exhibition?p=home")
            extracted = self.extract_import(response)

            runtime_year = int(extracted["ctl00$body$ddlYear"])
            now_quarter = int(extracted["ctl00$body$ddlMoth"])

            responses.append(TwTcResponse(year=runtime_year, text=response.text))

            next_quarter = get_next_element([1, 2, 3, 4], now_quarter)
            runtime_year += 1 if next_quarter < now_quarter else 0

            extracted["ctl00$body$ddlYear"] = str(runtime_year)
            extracted["ctl00$body$ddlMoth"] = str(next_quarter)

            next_response = await client.post(
                "https://twtc.com.tw/exhibition?p=home", data=extracted
            )
            responses.append(TwTcResponse(year=runtime_year, text=next_response.text))

        return responses

    async def fetch_parsed(self):
        this_translation = self.translation()
        responses: list[TwTcResponse] = self.response
        for response in responses:
            response.parsed = this_translation.translation_to_object(response.text)
            response.items = response.parsed.select("#home > div > table > tbody > tr")
        return responses

    async def fetch_items(self, *args, **kwargs):
        exhibition_items = []
        for response in self.parsed_:
            for item in response.items:
                data = self.use_parse(item).parse_to_base_model(
                    ExhibitionItem, year=response.year
                )
                if data.source_url is None:
                    continue
                exhibition_items.append(data)

        ok_items = []
        now_date = date_now()
        for item in exhibition_items:
            end_date_string = item.date.split("~")[-1].strip()
            end_date = datetime.datetime.strptime(end_date_string, "%Y-%m-%d").date()
            if end_date >= now_date:
                ok_items.append(item)
        return ok_items


async def main():
    await TwTcRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
