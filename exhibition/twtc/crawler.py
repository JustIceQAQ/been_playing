from typing import Optional
import httpx
from bs4 import BeautifulSoup, Tag

from exhibition.twtc.header import TWTCHeader


class TWTCCrawler:
    def __init__(self, url: str):
        self.url = url
        self._view_state_generator: Optional[str] = None
        self._event_validation: Optional[str] = None
        self._view_state: Optional[str] = None
        self.header = TWTCHeader().get_header()
        self.response_set: list["BeautifulSoup"] = []

    def _is_first(self) -> bool:
        return bool(self._view_state_generator and self._event_validation and self._view_state)

    def _reload_payload(self, parsed_response: "BeautifulSoup"):
        view_state_generator = parsed_response.find("input", {"id": "__VIEWSTATEGENERATOR"})
        self._view_state_generator = view_state_generator["value"]

        event_validation = parsed_response.find("input", {"id": "__EVENTVALIDATION"})
        self._event_validation = event_validation["value"]

        view_state = parsed_response.find("input", {"id": "__VIEWSTATE"})
        self._view_state = view_state["value"]

    def first_time_run_case(self) -> Optional["BeautifulSoup"]:
        response = httpx.get(self.url, headers=self.header)
        if response.is_success:
            parsed_response = BeautifulSoup(response.text, "html5lib")
            self._reload_payload(parsed_response)
            return parsed_response
        return None

    def second_time_run_case(self, year_value: int, month_value: int) -> Optional["BeautifulSoup"]:
        payload = {
            "__EVENTTARGET": "ctl00$body$ddlMoth",
            "__VIEWSTATE": self._view_state,
            "__VIEWSTATEGENERATOR": self._view_state_generator,
            "__EVENTVALIDATION": self._event_validation,
            "ctl00$body$ddlYear": year_value,
            "ctl00$body$ddlMoth": month_value
        }
        response = httpx.post(self.url, data=payload, headers=self.header)
        if response.is_success:
            parsed_response = BeautifulSoup(response.text, "html5lib")
            self._reload_payload(parsed_response)
            return parsed_response
        return None

    def run(self):
        first_time_run_result = self.first_time_run_case()
        self.response_set.append(first_time_run_result)

        year = first_time_run_result.find("select", {"id": "body_ddlYear", }).find("option", {"selected": "selected"})
        year_selected = int(year["value"])
        runtime_options = first_time_run_result.find("select", {"id": "body_ddlMoth", }).find("option", selected=True)
        next_options = [item for item in runtime_options.next_siblings if isinstance(item, Tag)]
        for option in next_options:
            second_time_run_result = self.second_time_run_case(year_selected, int(option["value"]))
            self.response_set.append(second_time_run_result)
