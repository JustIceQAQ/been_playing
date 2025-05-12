import asyncio
import datetime

import bs4

from app.platform.bookstickets.parse import BooksTicketsParse
from helpers.cache import NoneCache
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.headers_helper import get_header
from helpers.image.none.helper import NoneImage
from helpers.runner.helper import RunnerInit
from helpers.storage.helper import ExhibitionItem, Information
from helpers.translation.beautiful_soup import BeautifulSoupTranslation
from helpers.utils_helper import month_3, get_asyncio_rate_limit


class BooksTicketsRunner(RunnerInit):
    translation = BeautifulSoupTranslation
    use_parse = BooksTicketsParse
    use_suffix_item_from_url_auto = True

    def set_cache_expire(self) -> int | None:
        return month_3()

    def set_information(self) -> "Information":
        return Information(
            fullname="博客來售票網",
            code_name="BooksTickets",
            external_link="https://tickets.books.com.tw/leisure/",
        )

    async def fetch_response(self):
        headers = get_header()
        async with HttpxAsyncClient(headers=headers) as client:
            response = await client.get("https://tickets.books.com.tw/leisure/")
        return response.text

    async def fetch_parsed(self):
        parsed: bs4.BeautifulSoup = await super().fetch_parsed()
        return parsed.select("ul.prd > li")

    async def suffix_item_from_url_auto(self, items: list[ExhibitionItem]):
        headers = get_header()
        asyncio_limit = get_asyncio_rate_limit(3, 30)

        async with HttpxAsyncClient(headers=headers) as client, asyncio_limit:
            response_tasks = [client.get(item.source_url) for item in items]
            responses = await asyncio.gather(*response_tasks)

        parsers = [
            self.translation().translation_to_object(response.text)
            for response in responses
        ]

        for parsed, item in zip(parsers, items):
            lis = parsed.select("ul.prd002 > li")
            for li in lis:
                if li.find("span") is None:
                    continue
                span_text = li.find("span").get_text()
                if "活動地點" in span_text:
                    item.address = li.find("dfn").get_text()
                    continue
                elif "演出時間" in span_text:
                    date_string = li.find("dfn").get_text()
                    start_datetime_string, end_datetime_string = date_string.split("~")
                    start_date = datetime.datetime.strptime(
                        start_datetime_string.strip(), "%Y/%m/%d %H:%M"
                    ).strftime("%Y-%m-%d")
                    end_date = datetime.datetime.strptime(
                        end_datetime_string.strip(), "%Y/%m/%d %H:%M"
                    ).strftime("%Y-%m-%d")
                    item.date = f"{start_date} ~ {end_date}"
                    continue
                else:
                    continue


async def main():
    await BooksTicketsRunner().run(NoneCache(), NoneImage())


if __name__ == "__main__":
    asyncio.run(main())
