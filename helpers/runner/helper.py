import abc
import hashlib
import json
from typing import Any

from helpers.parse_helper import ParseInit as ParseInit2
from helpers.storage.helper import Exhibition, ExhibitionItem, Information
from helpers.translation.base import TranslationInit
from helpers.translation.json import JsonTranslation


class RunnerInit3(abc.ABC):
    translation: type[TranslationInit] = JsonTranslation
    use_parse: type[ParseInit2]

    @abc.abstractmethod
    def set_information(self) -> "Information":
        raise NotImplementedError

    @abc.abstractmethod
    async def fetch_response(self):
        raise NotImplementedError

    async def fetch_parsed(self) -> list[Any] | Any:
        if isinstance(self.response, list):
            return [self.translation().translation_to_object(i) for i in self.response]
        else:
            return self.translation().translation_to_object(self.response)

    async def fetch_items(self):
        exhibition_items = []
        for item in self.parsed_:
            data = self.use_parse(item).parse_to_base_model(ExhibitionItem)
            if data.source_url is None:
                continue
            exhibition_items.append(data)
        return exhibition_items

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

    async def cache_image_url(self, item: ExhibitionItem):
        hash_source_url = hashlib.sha256(item.source_url.encode("utf-8")).hexdigest()
        cache_figure_url = await self.cache.get(hash_source_url)
        if cache_figure_url:
            item.figure = cache_figure_url
        else:
            response = await self.image.upload(item.figure)
            if response.success:
                await self.cache.set(hash_source_url, response.data.webp_link)
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

        return hashlib.md5(content.encode("utf-8")).hexdigest()

    async def run(self, cache, image):
        self.cache = cache
        self.image = image
        self.information_ = self.set_information()
        self.response_ = await self.fetch_response()
        self.parsed_ = await self.fetch_parsed()
        self.items_ = await self.fetch_items()
        self.exhibition_ = Exhibition(information=self.information_, items=self.items)
        for item in self.exhibition_.items:
            await self.cache_image_url(item)

        await self.exhibition_.save_to_local(f"{self.information_.code_name}_v2")
