import abc
import logging
import os
import pathlib
from enum import Enum

import requests
from dotenv import load_dotenv


class NotifyInit(abc.ABC):
    @abc.abstractmethod
    def send_message(self, text):
        raise NotImplementedError


class NoneNotify(NotifyInit):
    def __init__(self):
        pass

    def send_message(self, message, *args, **kwargs):
        pass


class LogNotify(NotifyInit):
    class LogLevel(int, Enum):
        CRITICAL = logging.CRITICAL
        FATAL = logging.CRITICAL
        ERROR = logging.ERROR
        WARNING = logging.WARNING
        WARN = logging.WARN
        INFO = logging.INFO
        DEBUG = logging.DEBUG
        NOTSET = logging.NOTSET

    def __init__(self, runtime_log: logging.Logger):
        self.runtime_log: logging.Logger = runtime_log

    def send_message(self, message, level=logging.DEBUG, *args, **kwargs):
        self.runtime_log.log(level, message)


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

    def send_message(self, message, *args, **kwargs):
        data = {"message": f"{self.pre_text}\n{message}"}
        requests.post(self.service_path, headers=self.headers, data=data)


if __name__ == "__main__":
    this_env = pathlib.Path(__file__).parent.parent / ".env"
    if this_env.exists():
        load_dotenv(this_env)
    IS_DEBUG = os.getenv("IS_DEBUG", False)

    logging.basicConfig(
        level=logging.DEBUG if IS_DEBUG else logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )

    runtime_logging = logging.getLogger("runtime_logging")
    runtime_notify = LogNotify(runtime_logging)

    # LINE_NOTIFY_API = os.getenv("LINE_NOTIFY_API", None)
    # line_notify = LineNotify(LINE_NOTIFY_API)
    runtime_notify.send_message("0.0")
