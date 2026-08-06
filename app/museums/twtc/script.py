import asyncio
import datetime
from typing import cast

from app.museums.twtc.information import TwTcInformation
from app.museums.twtc.parse import TwTcParse
from app.museums.twtc.schemas import TwTcResponse
from app.museums.twtc.utils import get_next_element
from helpers.crawler.headers_helper import generate_headers
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import ExhibitionItem, Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import get_date, month_3


class TwTcRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = TwTcParse

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return TwTcInformation.get_information()

    def extract_import(self, response) -> dict:
        parsed = self.translation().translation_to_object(response.text)
        if parsed is None:
            return {}
        view_state = parsed.find("input", attrs={"name": "__VIEWSTATE"})["value"]
        view_state_generator = parsed.find("input", attrs={"name": "__EVENTVALIDATION"})["value"]
        event_validation = parsed.find("input", attrs={"name": "__EVENTVALIDATION"})["value"]
        selected_year = parsed.find("select", attrs={"id": "body_ddlYear"}).find("option", {"selected": "selected"})[
            "value"
        ]
        selected_month = parsed.find("select", attrs={"id": "body_ddlMoth"}).find("option", {"selected": "selected"})[
            "value"
        ]
        return {
            "__VIEWSTATE": view_state,
            "__VIEWSTATEGENERATOR": view_state_generator,
            "__EVENTVALIDATION": event_validation,
            "ctl00$body$ddlYear": selected_year,
            "ctl00$body$ddlMoth": selected_month,
        }

    async def fetch_response(self):
        headers = generate_headers(
            host="twtc.com.tw",
            referer="https://twtc.com.tw/exhibition?p=home",
            other_headers={
                "Pragma": "no-cache",
            },
        )
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

            next_response = await client.post("https://twtc.com.tw/exhibition?p=home", data=extracted)
            responses.append(TwTcResponse(year=runtime_year, text=next_response.text))

        return responses

    async def fetch_parsed(self) -> list[TwTcResponse]:
        this_translation = self.translation()
        responses: list[TwTcResponse] = self.response
        for response in responses:
            this_translation_data = this_translation.translation_to_object(response.text)
            if this_translation_data is None:
                continue
            response.parsed = this_translation_data
            response.items = response.parsed.select("#home > div > table > tbody > tr")

        return responses

    async def fetch_items(self, *args, **kwargs):
        exhibition_items = []
        responses = cast(list[TwTcResponse], self.parsed_)
        for response in responses:
            for item in response.items:
                data = self.use_parse(item).parse_to_base_model(ExhibitionItem, year=response.year)
                if data.source_url is None:
                    continue
                exhibition_items.append(data)

        ok_items = []
        now_date = get_date.now
        for item in exhibition_items:
            if item.date is None:
                continue
            end_date_string = item.date.split("~")[-1].strip()
            end_date = datetime.datetime.strptime(end_date_string, "%Y-%m-%d").date()
            if end_date >= now_date:
                ok_items.append(item)
        return ok_items


async def main():
    from helpers.cache.none.helper import none_cache
    from helpers.image_hosting.none.helper import none_image_hosting

    await TwTcRunner().run(none_cache, none_image_hosting)


if __name__ == "__main__":
    asyncio.run(main())
