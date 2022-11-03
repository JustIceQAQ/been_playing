import abc
import os
import pathlib

import requests
from dotenv import load_dotenv


class NotifyInit(abc.ABC):
    @abc.abstractmethod
    def send_message(self, text):
        raise NotImplementedError


class LineNotify(NotifyInit):
    def __init__(self, token: str):
        self.service_path = "https://notify-api.line.me/api/notify"
        self.token = token
        self.check()
        self.headers = {"Authorization": "Bearer " + self.token}
        self.pre_text = "【been play】"

    def check(self):
        if self.token is None:
            raise ValueError("token is empty.")

    def send_message(self, message):
        data = {"message": f"{self.pre_text}\n{message}"}
        requests.post(self.service_path, headers=self.headers, data=data)


if __name__ == "__main__":
    this_env = pathlib.Path(__file__).parent.parent / ".env"
    if this_env.exists():
        load_dotenv(this_env)
    LINE_NOTIFY_API = os.getenv("LINE_NOTIFY_API", None)
    line_notify = LineNotify(LINE_NOTIFY_API)
    line_notify.send_message("0.0")
