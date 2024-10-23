import uuid
from pathlib import Path

from aiofile import async_open
from pydantic import BaseModel, Field, model_validator

from helpers.utils_helper import datetime_now_iso_format


def hex_uuid5(value: str) -> str:
    return uuid.uuid5(uuid.UUID("00000000-0000-0000-0000-000000000000"), value).hex


class ExhibitionItem(BaseModel):
    title: str | None = None
    date: str | None = None
    address: str | None = None
    figure: str | None = None
    source_url: str | None = None
    UUID: str | None = None

    @model_validator(mode="after")
    def generate_uuid(cls, values):
        if values.source_url is not None:
            values.UUID = hex_uuid5(values.source_url)
        return values


class Information(BaseModel):
    fullname: str
    code_name: str
    external_link: str


class Exhibition(BaseModel):
    information: Information
    counts: int = 0
    items: list[ExhibitionItem] | None = Field(default_factory=list)
    last_update: str | None = Field(default_factory=datetime_now_iso_format)
    visit: dict[str, str] | None = Field(default_factory=dict)

    @model_validator(mode="after")
    def generate_counts(cls, values):
        values.counts = len(values.items)
        return values

    async def save_to_local(
        self,
        filename: str,
        folder: str | Path | None = Path(__file__).parent.parent.parent.absolute()
        / "data"
        / "v2",
    ):
        async with async_open(folder / f"{filename}.json", "w+") as afp:
            await afp.write(self.model_dump_json())
