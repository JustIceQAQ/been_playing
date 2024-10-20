import abc


class RunnerInit3(abc.ABC):
    @abc.abstractmethod
    async def get_response(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_parsed(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_items(self):
        raise NotImplementedError

    async def run(self):
        pass
        # response = await self.get_response()
        # parsed = await self.get_parsed()
        # items = await self.get_items()
