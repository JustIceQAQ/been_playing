import niquests


class NiquestsAsyncSession(niquests.AsyncSession):
    def __init__(
        self,
        timeout: int | None | niquests.Timeout = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(timeout=timeout, *args, **kwargs)
        self.passed_args = args
        self.passed_kwargs = kwargs

    async def __aenter__(self) -> niquests.AsyncSession:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
