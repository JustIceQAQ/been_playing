import abc
import asyncio
import hashlib
import json
import time
from typing import Any, TYPE_CHECKING
from helpers.parse_helper import ParseInit
from helpers.storage.helper import Exhibition, ExhibitionItem, Information

from helpers.suffix_helper import suffix_helper
from helpers.translation.base import TranslationInit
from helpers.translation.json import JsonTranslation
from helpers.cache.base import Cache

if TYPE_CHECKING:
    from helpers.storage.social_media import SocialMedia


class RunnerInit(abc.ABC):
    translation: type[TranslationInit] = JsonTranslation
    use_parse: type[ParseInit]
    use_suffix_item_from_file_func: bool = False
    use_suffix_item_from_url_auto: bool = False
    is_unique: bool = True
    is_sort: bool = True
    output_rss: bool = False
    output_ics: bool = False

    retry_on_empty: bool = True
    retry_times: int = 3
    retry_interval: int = 10

    def set_cache_expire(self) -> int | None:
        return None

    @abc.abstractmethod
    def set_information(self) -> "Information":
        raise NotImplementedError

    @abc.abstractmethod
    def set_social_media(self) -> "SocialMedia":
        pass

    @abc.abstractmethod
    async def fetch_response(self):
        raise NotImplementedError

    async def items_check(self):
        if not self.items_:
            import sentry_sdk

            class_name = self.__class__.__name__
            sentry_sdk.capture_message(f"{class_name} items is empty")

    async def fetch_parsed(self, *args, **kwargs) -> list[Any] | Any | dict[str, list[Any]]:
        this_translation = self.translation()
        if isinstance(self.response, list):
            responses = self.response
            return [
                this_translation.translation_to_object(response, *args, **kwargs) if response is not None else None
                for response in responses
            ]
        elif isinstance(self.response, dict) and all(isinstance(i, list) for i in self.response.values()):
            translation_data = {}
            for key in self.response.keys():
                translation_data[key] = []
            for key, value in self.response.items():
                for v in value:
                    translation_data[key].append(this_translation.translation_to_object(v, *args, **kwargs))
            return translation_data
        else:
            return self.translation().translation_to_object(self.response, *args, **kwargs)

    async def fetch_items(self, *args, **kwargs):
        exhibition_items = []
        for item in self.parsed_:
            data = self.use_parse(item).parse_to_base_model(ExhibitionItem, *args, **kwargs)
            if data.source_url is None:
                continue
            exhibition_items.append(data)
        return exhibition_items

    async def suffix_item_from_url_auto(self, items: list[ExhibitionItem]):
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

    async def cache_image_url(self, item: ExhibitionItem, sem: asyncio.Semaphore):
        async with sem:
            hash_source_url = hashlib.sha256(item.source_url.encode("utf-8")).hexdigest()
            cache_figure_url = await self.cache.aget(hash_source_url)
            if cache_figure_url:
                item.figure = cache_figure_url
            else:
                if item.figure:
                    result = await self.image.upload(item.figure)
                    if result:
                        await self.cache.aset(
                            hash_source_url,
                            result,
                            expire=self.set_cache_expire(),
                        )
                        item.figure = result
                    else:
                        pass

    def hash_content(self, content: str | dict):
        if isinstance(content, dict):
            content = json.dumps(content, sort_keys=True)
        elif not isinstance(content, str):
            raise ValueError("Content must be a string or a dictionary")

        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    async def run(
        self,
        cache: Cache,
        image,
        prefix: str | None = None,
        image_sem: asyncio.Semaphore | None = None,
        develop_mode: bool = False,
    ):
        start_time = time.time()
        try:
            self.cache = cache
            self.image = image
            self.information_ = self.set_information()

            if self.output_rss:
                self.information_.has_rss = True
            if self.output_ics:
                self.information_.has_ics = True

            self.response_ = await self.fetch_response()
            self.parsed_ = await self.fetch_parsed()
            self.items_ = await self.fetch_items()

            if self.retry_on_empty:
                for attempt in range(1, self.retry_times + 1):
                    if self.items_:
                        break
                    await asyncio.sleep(self.retry_interval * attempt)
                    self.response_ = await self.fetch_response()
                    self.parsed_ = await self.fetch_parsed()
                    self.items_ = await self.fetch_items()

            self.exhibition_ = Exhibition(
                information=self.information_, items=self.items_, social_media=self.set_social_media()
            )

            _image_sem = image_sem if image_sem is not None else asyncio.Semaphore(5)
            cache_tasks = [self.cache_image_url(item, _image_sem) for item in self.exhibition_.items]
            await asyncio.gather(*cache_tasks)

            if self.use_suffix_item_from_url_auto:
                await self.suffix_item_from_url_auto(self.exhibition_.items)
            if self.use_suffix_item_from_file_func:
                await self.suffix_item_from_file(self.exhibition_.items)

            end_time = time.time()
            execution_time = end_time - start_time

            await self.items_check()

            await self.exhibition_.save_to_json(
                f"{self.information_.code_name}",
                execution_time=execution_time,
                is_unique=self.is_unique,
                is_sort=self.is_sort,
                prefix=prefix,
            )
            if self.output_rss:
                await self.exhibition_.save_to_rss()
            if self.output_ics:
                await self.exhibition_.save_to_ics()
            if develop_mode:
                print(self.exhibition_)

        except Exception as e:  # noqa F841
            class_name = self.__class__.__name__
            raise RuntimeError(f"[{class_name}] 執行失敗") from e
