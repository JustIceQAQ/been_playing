import abc

from helpers.storage.helper import Information


class RunnerInit3(abc.ABC):

    @abc.abstractmethod
    def set_information(self) -> "Information":
        raise NotImplementedError

    @abc.abstractmethod
    async def fetch_response(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def fetch_parsed(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def fetch_items(self):
        raise NotImplementedError

    @property
    def information(self):
        return self.information_

    @property
    def response(self):
        return self.response_

    @property
    def parsed(self):
        return self.parsed_

    @property
    def items(self):
        return self.items_

    async def run(self):
        self.information_ = self.set_information()
        self.response_ = await self.fetch_response()
        self.parsed_ = await self.fetch_parsed()
        self.items_ = await self.fetch_items()
