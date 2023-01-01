import datetime
import re
from pathlib import Path

import pytz

from exhibition import ExhibitionEnum
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
        requests_worker = self.instantiation(self.target_url)
        headers = (
            self.use_header().get_header() if self.use_header is not None else None
        )
        return requests_worker.fetch(self.use_method, headers=headers)

    def get_items(self, response):
        return response.select("#home > div > table > tbody > tr")

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
