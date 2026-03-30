import niquests
from niquests.adapters import AsyncHTTPAdapter
from urllib3.util import Retry

_RETRY_STRATEGY = Retry(
    read=3,
    connect=3,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET", "POST", "PUT"],
    backoff_factor=0.5,
    raise_on_status=False,
)
_ADAPTER = AsyncHTTPAdapter(max_retries=_RETRY_STRATEGY)


class NiquestsAsyncSession(niquests.AsyncSession):
    def __init__(
        self,
        timeout: int | None | niquests.Timeout = 300,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(timeout=timeout, *args, **kwargs)
        self.passed_args = args
        self.passed_kwargs = kwargs

        self.mount("https://", _ADAPTER)
        self.mount("http://", _ADAPTER)

    async def __aenter__(self) -> niquests.AsyncSession:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
