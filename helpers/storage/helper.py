import datetime
import re
import uuid
from decimal import Decimal
from pathlib import Path
from typing import Any

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
    tags: list[str] | None = Field(default_factory=list)
    UUID: str | None = None

    @model_validator(mode="after")
    def generate_uuid(cls, values):
        if values.source_url is not None:
            values.UUID = hex_uuid5(values.source_url)
        return values

    def extract_date_type(self) -> int:
        """
        回傳數字分類型，數字越小排序越前面
        - 0: 有開始與結束日期（範圍型）
        - 1: 只有單一天日期
        - 2: 無法判斷日期（None 或其他不明格式）
        - 3: 開始日期為永久展（只有起始無結束）
        """
        if self.date is None:
            return 2

        if re.match(r"\d{4}-\d{2}-\d{2}\s*~\s*\d{4}-\d{2}-\d{2}", self.date):
            return 0
        elif re.match(r"\d{4}-\d{2}-\d{2}\s*~\s*", self.date):
            return 3
        elif re.match(r"\d{4}-\d{2}-\d{2}$", self.date):
            return 1
        else:
            return 2

    def extract_start_date(self) -> datetime.datetime | None:
        if self.date is None:
            return None
        match = re.match(r"(\d{4}-\d{2}-\d{2})", self.date)
        if match:
            try:
                return datetime.datetime.strptime(match.group(1), "%Y-%m-%d")
            except ValueError:
                return None
        return None

    def count_none_fields(self) -> int:
        return sum(
            1
            for field in [
                self.title,
                self.date,
                self.address,
                self.figure,
                self.source_url,
                self.tags,
                self.UUID,
            ]
            if field is None
        )

    def __lt__(self, other: "ExhibitionItem") -> bool:
        self_type = self.extract_date_type()
        other_type = other.extract_date_type()

        if self_type != other_type:
            return self_type < other_type

        if self_type in (0, 1, 3):
            self_date = self.extract_start_date()
            other_date = other.extract_start_date()
            if self_date and other_date:
                return self_date < other_date
            elif self_date and not other_date:
                return True
            elif not self_date and other_date:
                return False
            else:
                return False
        elif self_type == 2:
            return self.count_none_fields() < other.count_none_fields()

        return False  # fallback

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExhibitionItem):
            return NotImplemented
        return all(
            getattr(self, field) == getattr(other, field)
            for field in self.model_fields.keys()
        )

    def __hash__(self):
        values = []
        for field, value in self.model_fields.items():
            val = getattr(self, field)
            try:
                hash(val)  # 測試是否可 hash
                values.append(val)
            except TypeError:
                # 忽略不可 hash 的值
                continue
        return hash(tuple(values))


class Coordinate(BaseModel):
    raw_coordinates: str | None = None
    longitude: Decimal = Field(default=None, description="經度")
    latitude: Decimal = Field(default=None, description="緯度")
    google_map_place_id: str | None = Field(
        default=None, description="Google Map Place ID"
    )
    name: str | None = Field(
        default=None, description="名稱, 若為None 則代表該地點沒有分館"
    )

    @model_validator(mode="before")
    @classmethod
    def process_coordinates(cls, data: Any) -> Any:
        if isinstance(data, dict):
            raw_coords = data.get("raw_coordinates")
            if raw_coords and isinstance(raw_coords, str):
                try:
                    parts = raw_coords.split(", ")
                    if len(parts) == 2:
                        lat_str, lon_str = parts
                        data["latitude"] = lat_str
                        data["longitude"] = lon_str

                except Exception as e:
                    print(f"座標解析失敗: {e}")
                    pass

        return data


class Information(BaseModel):
    fullname: str
    code_name: str
    external_link: str
    branch_coordinates: Coordinate | list[Coordinate] | None = Field(
        default=None, description="經緯度"
    )
    location_code: str | None = Field(default=None, description="ISO 3166/MA")


class Exhibition(BaseModel):
    information: Information
    counts: int = 0
    items: list[ExhibitionItem] = Field(default_factory=list)
    last_update: str = Field(default_factory=datetime_now_iso_format)
    execution_time: float | None = Field(default=None)

    @model_validator(mode="after")
    def generate_counts(cls, values):
        values.counts = len(values.items)
        return values

    def deduplicate_items(self, items: list[ExhibitionItem]) -> list[ExhibitionItem]:
        return list(dict.fromkeys(items))

    async def save_to_local(
        self,
        filename: str,
        folder: str | Path | None = Path(__file__).parent.parent.parent.absolute()
        / "data"
        / "v2",
        execution_time: float | None = None,
        is_unique: bool | None = True,
        is_sort: bool | None = True,
        prefix: str | None = None,
    ):
        if is_unique:
            self.items = self.deduplicate_items(self.items)
        if is_sort:
            self.items.sort()
        this_folder = folder
        if prefix is not None:
            this_folder = (
                Path(__file__).parent.parent.parent.absolute() / "data" / prefix
            )
            this_folder.mkdir(exist_ok=True)
        self.execution_time = execution_time
        async with async_open(this_folder / f"{filename}.json", "w+") as afp:
            await afp.write(self.model_dump_json())
