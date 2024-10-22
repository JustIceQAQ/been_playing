import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    IS_DEBUG: bool = Field(description="DEBUG 模式", default=False)

    IMGUR_API_CLIENT_ID: str
    IMGUR_API_CLIENT_SECRET: str

    SCRAPER_API_KEY: str
    SCRAPE_DO_API_KEY: str

    LINE_NOTIFY_API: str

    SENTRY_SDK_DNS: str


class LocalSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class ActionSettings(Settings):
    pass


@lru_cache
def get_settings() -> Settings:
    is_debug = os.getenv("IS_DEBUG")
    if is_debug:
        return LocalSettings()
    return ActionSettings()
