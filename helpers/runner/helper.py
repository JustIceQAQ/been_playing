import abc


class RunnerInit3(abc.ABC):
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
    def response(self):
        return self.response_

    @property
    def parsed(self):
        return self.parsed_

    @property
    def items(self):
        return self.items_

    async def run(self):
        self.response_ = await self.fetch_response()
        self.parsed_ = await self.fetch_parsed()
        self.items_ = await self.fetch_items()
