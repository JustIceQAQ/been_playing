import uuid
from pathlib import Path

from aiofile import async_open
from pydantic import BaseModel, Field, model_validator


def hex_uuid5(value: str) -> str:
    return uuid.uuid5(uuid.UUID("00000000-0000-0000-0000-000000000000"), value).hex


class ExhibitionData(BaseModel):
    title: str | None = None
    date: str | None = None
    address: str | None = None
    figure: str | None = None
    source_url: str
    UUID: str | None = None

    @model_validator(mode="after")
    def generate_uuid(cls, values):
        values.UUID = hex_uuid5(values.source_url)
        return values


class Information(BaseModel):
    fullname: str
    code_name: str
    external_link: str


class Exhibition(BaseModel):
    information: Information
    counts: int = 0
    data: list[ExhibitionData] | None = Field(default_factory=list)
    last_update: str | None = None
    visit: dict[str, str] | None = Field(default_factory=dict)

    @model_validator(mode="after")
    def generate_counts(cls, values):
        values.counts = len(values.data)
        return values

    async def save_to_local(
        self,
        filename: str,
        folder: str | Path | None = Path(__file__).parent.parent.parent.absolute()
        / "data",
    ):
        async with async_open(folder / f"{filename}.json", "w+") as afp:
            await afp.write(self.model_dump_json())
