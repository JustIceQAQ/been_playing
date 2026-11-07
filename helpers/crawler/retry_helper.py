import asyncio
import logging
from collections.abc import Awaitable, Callable

import httpx2
import niquests
import wreq

logger = logging.getLogger(__name__)


RETRYABLE_EXCEPTIONS: tuple[type[BaseException], ...] = (
    # --- httpx2 ---
    httpx2.NetworkError,  # ConnectError / ReadError / WriteError / CloseError
    httpx2.TimeoutException,  # ConnectTimeout / ReadTimeout / WriteTimeout / PoolTimeout
    httpx2.RemoteProtocolError,
    httpx2.ProxyError,
    # --- niquests(例外繼承 OSError;不是內建的 ConnectionError)---
    niquests.ConnectionError,  # 含 ConnectTimeout
    niquests.Timeout,  # 含 ReadTimeout / ConnectTimeout
    # --- wreq(例外彼此獨立,沒有共同父類別)---
    wreq.ConnectionError,
    wreq.ConnectionResetError,
    wreq.ProxyConnectionError,
    wreq.TimeoutError,
)


def is_retryable(exc: BaseException) -> bool:
    return isinstance(exc, RETRYABLE_EXCEPTIONS)


def _record(name: str, attempt: int, total: int, exc: BaseException, delay: float) -> None:
    message = (
        f"{name} 連線失敗 ({type(exc).__module__}.{type(exc).__name__}: {exc}),第 {attempt}/{total} 次,{delay}s 後重試"
    )
    logger.warning(message)
    try:
        import sentry_sdk

        sentry_sdk.add_breadcrumb(category="retry", level="warning", message=message)
    except Exception:  # noqa: BLE001  記錄失敗不能影響主流程
        pass


async def call_with_retry[T](
    func: Callable[[], Awaitable[T]],
    *,
    retries: int = 3,
    interval: float = 10,
    name: str = "request",
) -> T:
    """呼叫 func();遇到連線層例外時最多重試 `retries` 次(共 retries + 1 次嘗試)。

    等待時間為 interval * 第幾次重試(線性退避)。重試用盡後重新拋出最後一次的原始例外,
    讓上層(Sentry)看到真正的錯誤與 traceback。
    """
    total = retries + 1
    for attempt in range(1, total + 1):
        try:
            return await func()
        except RETRYABLE_EXCEPTIONS as exc:
            if attempt >= total:
                raise
            delay = interval * attempt
            _record(name, attempt, total, exc, delay)
            await asyncio.sleep(delay)
    raise RuntimeError("unreachable")  # pragma: no cover
