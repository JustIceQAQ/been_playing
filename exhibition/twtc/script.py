import datetime
import re
from pathlib import Path

import pytz

from exhibition import ExhibitionEnum
from exhibition.twtc.crawler import TWTCCrawler
from exhibition.twtc.header import TWTCHeader
from exhibition.twtc.parse import TWTCParse
from helper.clean_helper import RequestsClean
from helper.instantiation_helper import RequestsBeautifulSoupInstantiation
from helper.runner_helper import RunnerInit


class TWTCRunner(RunnerInit):
    """台北世貿中心"""

    root_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    target_url = "https://twtc.com.tw/exhibition?p=home"
    use_method = "GET"
    target_storage = str(root_dir / "data" / "twtc_exhibition.json")
    target_systematics = ExhibitionEnum.TWTC
    instantiation = RequestsBeautifulSoupInstantiation
    use_header = TWTCHeader
    use_parse = TWTCParse

    def get_response(self, *args, **kwargs):
        responses = TWTCCrawler(self.target_url)
        responses.run()
        if responses:
            return responses.response_set
        return []

    def get_items(self, responses):
        return sum(
            [
                response.select("#home > div > table > tbody > tr")
                for response in responses
            ],
            [],
        )

    def get_parsed(self, items):
        runtime_now = datetime.datetime.now(pytz.timezone("Asia/Taipei")).date()
        for item in items:
            data = self.use_parse(item).parsed()
            clean_data = {
                key: RequestsClean.clean_string(value) for key, value in data.items()
            }

            date_list = re.findall(r"(\d{2}\/\d{2})", clean_data["date"])
            if date_list:
                end_date = datetime.datetime.strptime(
                    f"{runtime_now.year}/{date_list[-1]} +0800", "%Y/%m/%d %z"
                ).date()
                if runtime_now > end_date:
                    continue

            exhibition = self.exhibition_model(
                systematics=self.target_systematics, **clean_data
            )
            yield exhibition


if __name__ == "__main__":
    t = TWTCRunner()
    t.run()
