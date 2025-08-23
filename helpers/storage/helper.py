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
        is_unique: bool | None = True,
        is_sort: bool | None = True,
    ):
        if is_unique:
            self.items = self.deduplicate_items(self.items)
        if is_sort:
            self.items.sort()

        async with async_open(folder / f"{filename}.json", "w+") as afp:
            await afp.write(self.model_dump_json())
