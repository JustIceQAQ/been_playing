import datetime
import re
import uuid
from pathlib import Path

from aiofile import async_open
from pydantic import BaseModel, Field, model_validator

from helpers.utils_helper import datetime_now_iso_format


def hex_uuid5(value: str) -> str:
    return uuid.uuid5(uuid.UUID("00000000-0000-0000-0000-000000000000"), value).hex


def extract_start_date(date_str: str | None) -> datetime.datetime | None:
    """
    從 date 字串中擷取開始日期
    例如：
        "2025-04-03 ~ 2025-05-04" -> datetime(2025, 4, 3)
        "2025-03-28 ~" -> datetime(2025, 3, 28)
        "2025-03-28" -> datetime(2025, 3, 28)
        None -> None
    """
    if not date_str:
        return None
    match = re.match(r"(\d{4}-\d{2}-\d{2})", date_str)
    if match:
        return datetime.datetime.strptime(match.group(1), "%Y-%m-%d")
    return None


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

    def count_none_fields(self) -> int:
        return sum(1 for value in self.__dict__.values() if value is not None)

    def __lt__(self, other: "ExhibitionItem") -> bool:
        # 若 date 是 None，直接排到後面
        self_date = extract_start_date(self.date)
        other_date = extract_start_date(other.date)

        if self_date is None and other_date is not None:
            return False
        if self_date is not None and other_date is None:
            return True
        if self_date is not None and other_date is not None:
            return self_date < other_date

        # 若兩者都是 None，就看 None 欄位數
        return self.count_none_fields() < other.count_none_fields()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExhibitionItem):
            return NotImplemented
        return all(
            getattr(self, field) == getattr(other, field)
            for field in self.model_fields.keys()
        )

    def __hash__(self):
        # 所有欄位都納入 hash 計算，確保 set() 正常運作
        return hash(tuple(getattr(self, field) for field in self.model_fields.keys()))


class Information(BaseModel):
    fullname: str
    code_name: str
    external_link: str
    map_url: str | None = Field(default=None)
    address: str | None = Field(default=None)
    google_map_place_id: str | None = Field(default=None)


class Exhibition(BaseModel):
    information: Information
    counts: int = 0
    items: list[ExhibitionItem] = Field(default_factory=list)
    last_update: str = Field(default_factory=datetime_now_iso_format)
    visit: dict[str, str] = Field(default_factory=dict)

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
        self.items = list(set(self.items))
        self.items.sort()

        async with async_open(folder / f"{filename}.json", "w+") as afp:
            await afp.write(self.model_dump_json())
