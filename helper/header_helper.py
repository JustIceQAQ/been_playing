from abc import ABCMeta, abstractmethod

from fake_useragent import UserAgent

UA = UserAgent(browsers="chrome", os=["windows", "macos"], platforms="pc")


class HeaderInit(metaclass=ABCMeta):
    def get_random_user_agent(self) -> str:
        return UA.random

    @abstractmethod
    def get_header(self) -> dict[str, str] | None:
        raise NotImplementedError
