import asyncio
from functools import wraps


class AsyncLimiter:
    def __init__(self, delay: int = 8):
        """
        初始化限速器
        :param delay: 每次執行完 async 函數後的延遲時間，默認為 8 秒
        """
        self.delay = delay
        self._lock = asyncio.Lock()

    async def call(self, func, *args, **kwargs):
        """
        執行帶限速的異步函數
        :param func: 要調用的異步函數
        :param args: 傳遞給函數的參數
        :param kwargs: 傳遞給函數的關鍵字參數
        :return: 函數執行結果
        """
        async with self._lock:
            result = await func(*args, **kwargs)
            await asyncio.sleep(self.delay)  # 延遲8秒後才允許下一個調用

        return result

    def limit(self, func):
        """
        作為裝飾器使用的限速器，限制裝飾的 async 函數執行頻率
        :param func: 要裝飾的異步函數
        :return: 包裹後的函數
        """

        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with self._lock:
                result = await func(*args, **kwargs)
                await asyncio.sleep(self.delay)
            return result

        return wrapper
