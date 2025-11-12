import abc
import asyncio
import hashlib
import json
import traceback
from typing import Any
import httpx
from helpers.crawler.httpx.helper import HttpxAsyncClient
from helpers.parse_helper import ParseInit as ParseInit2
from helpers.storage.helper import Exhibition, ExhibitionItem, Information
from helpers.suffix_helper import suffix_helper
from helpers.translation.base import TranslationInit
from helpers.translation.json import JsonTranslation
from helpers.cache.base import Cache


class RunnerInit(abc.ABC):
    translation: type[TranslationInit] = JsonTranslation
    use_parse: type[ParseInit2]
    use_suffix_item_from_file_func: bool = False
    use_suffix_item_from_url_auto: bool = False
    is_unique: bool = True
    is_sort: bool = True

    def set_cache_expire(self) -> int | None:
        return None

    @abc.abstractmethod
    def set_information(self) -> "Information":
        raise NotImplementedError

    @abc.abstractmethod
    async def fetch_response(self):
        raise NotImplementedError

    async def fetch_parsed(self, *args, **kwargs) -> list[Any] | Any:
        if isinstance(self.response, list):
            this_translation = self.translation()
            responses = self.response
            return [
                this_translation.translation_to_object(response, *args, **kwargs)
                if response is not None
                else None
                for response in responses
            ]
        else:
            return self.translation().translation_to_object(
                self.response, *args, **kwargs
            )

    async def fetch_items(self, *args, **kwargs):
        exhibition_items = []
        for item in self.parsed_:
            data = self.use_parse(item).parse_to_base_model(
                ExhibitionItem, *args, **kwargs
            )
            if data.source_url is None:
                continue
            exhibition_items.append(data)
        return exhibition_items

    async def suffix_item_from_url_auto(self, item: list[ExhibitionItem]):
        pass

    async def suffix_item_from_file(self, items: list[ExhibitionItem]):
        information = self.set_information()
        code = information.code_name
        suffix_data = suffix_helper.get_code_name_items(code)
        for item in items:
            this_suffix: dict | None = suffix_data.get(item.UUID, None)
            if this_suffix:
                for column in item.model_fields.keys():
                    this_column = this_suffix.get(column, None)
                    if this_column:
                        setattr(item, column, this_column)

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

    @property
    def exhibition(self):
        return self.exhibition_

    async def cache_image_url(self, item: ExhibitionItem, client: httpx.AsyncClient):
        async with asyncio.Semaphore(10):
            hash_source_url = hashlib.sha256(
                item.source_url.encode("utf-8")
            ).hexdigest()
            cache_figure_url = await self.cache.get(hash_source_url)
            if cache_figure_url:
                item.figure = cache_figure_url
            else:
                response = await self.image.upload(item.figure, client)
                if response.success:
                    await self.cache.set(
                        hash_source_url,
                        response.data.webp_link,
                        expire=self.set_cache_expire(),
                    )
                    item.figure = response.data.webp_link
                else:
                    pass

    def hash_content(self, content: str | dict):
        """生成頁面內容的哈希值，支持 str 和 dict 兩種格式"""
        if isinstance(content, dict):
            content = json.dumps(
                content, sort_keys=True
            )  # sort_keys=True 確保鍵的順序一致
        elif not isinstance(content, str):
            raise ValueError("Content must be a string or a dictionary")

        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    async def run(self, cache: Cache, image, prefix: str | None = None):
        try:
            self.cache = cache
            self.image = image
            self.information_ = self.set_information()
            self.response_ = await self.fetch_response()
            self.parsed_ = await self.fetch_parsed()
            self.items_ = await self.fetch_items()
            self.exhibition_ = Exhibition(
                information=self.information_, items=self.items_
            )
            try:
                async with HttpxAsyncClient() as client:
                    tasks = [
                        self.cache_image_url(item, client)
                        for item in self.exhibition_.items
                    ]
                    await asyncio.gather(*tasks)
            except Exception as e:  # noqa F841
                pass
            if self.use_suffix_item_from_url_auto:
                await self.suffix_item_from_url_auto(self.exhibition_.items)
            if self.use_suffix_item_from_file_func:
                await self.suffix_item_from_file(self.exhibition_.items)

            await self.exhibition_.save_to_local(
                f"{self.information_.code_name}",
                is_unique=self.is_unique,
                is_sort=self.is_sort,
                prefix=prefix,
            )
        except Exception as e:  # noqa F841
            print(traceback.format_exc())
