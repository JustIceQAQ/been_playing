import os
import pathlib
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    IS_DEBUG: bool | None = Field(description="DEBUG 模式", default=False)
    SCRAPER_API_KEY: list[str] | None = Field(default=None)
    SCRAPE_DO_API_KEY: str | None = Field(default=None)
    SENTRY_SDK_DNS: str | None = Field(default=None)
    PROXY_POOL: str | None = Field(default=None)
    CLOUDINARY_CLOUD_NAME: str | None = Field(default=None)
    CLOUDINARY_API_KEY: str | None = Field(default=None)
    CLOUDINARY_API_SECRET: str | None = Field(default=None)

    @property
    def is_cloudinary_available(self) -> bool:
        return all([self.CLOUDINARY_CLOUD_NAME, self.CLOUDINARY_API_KEY, self.CLOUDINARY_API_SECRET])

    class Config:
        case_sensitive = False


class LocalSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=pathlib.Path(__file__).parent.parent.absolute() / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class ActionSettings(Settings):
    pass


@lru_cache
def get_settings() -> Settings:
    is_debug = os.getenv("IS_DEBUG", "true").lower() in ("1", "true", "yes")
    if is_debug:
        return LocalSettings()
    return ActionSettings()
