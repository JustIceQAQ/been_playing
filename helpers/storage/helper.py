import datetime
import pathlib
import re
import uuid
from decimal import Decimal
from pathlib import Path
from typing import Any

import aiofiles
from pydantic import BaseModel, Field, model_validator
from feedgen.feed import FeedGenerator
from icalendar import Calendar, Event
from configs.settings import get_settings
from helpers.storage.symbol import TaiwanCity, VenueType
from helpers.utils_helper import (
    get_datetime_now,
    get_datetime_now_iso_format,
    get_timezone,
    get_timezone_str,
)


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


def orjson_default_handler(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError


def hex_uuid5(value: str) -> str:
    return uuid.uuid5(uuid.UUID("00000000-0000-0000-0000-000000000000"), value).hex


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
                return datetime.datetime.strptime(match.group(1), "%Y-%m-%d").replace(tzinfo=get_timezone())
            except ValueError:
                return None
        return None

    def extract_end_date(self) -> datetime.datetime | None:
        if self.date is None:
            return None
        match = re.search(r"~\s*(\d{4}-\d{2}-\d{2})", self.date)
        if match:
            try:
                this_date = match.group(1)
                return datetime.datetime.strptime(this_date, "%Y-%m-%d").replace(tzinfo=get_timezone())
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
        return all(getattr(self, field) == getattr(other, field) for field in self.model_fields.keys())

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
    location_code: TaiwanCity | None = Field(default=None, description="ISO 3166/MA")
    raw_coordinates: str | None = None
    longitude: Decimal = Field(default=None, description="經度")
    latitude: Decimal = Field(default=None, description="緯度")
    google_map_place_id: str | None = Field(default=None, description="Google Map Place ID")
    name: str | None = Field(default=None, description="名稱, 若為None 則代表該地點沒有分館")

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
    branch_coordinates: Coordinate | list[Coordinate] | None = Field(default=None, description="經緯度")
    location_code: TaiwanCity | None = Field(default=None, description="ISO 3166/MA")
    venue_type: VenueType | None = Field(default=None, description="場所類型")
    has_rss: bool | None = Field(default=False)
    has_ics: bool | None = Field(default=False)


class Exhibition(BaseModel):
    information: Information
    counts: int = 0
    items: list[ExhibitionItem] = Field(default_factory=list)
    last_update: str = Field(default_factory=get_datetime_now_iso_format)
    execution_time: float | None = Field(default=None)

    @model_validator(mode="after")
    def generate_counts(cls, values):
        values.counts = len(values.items)
        return values

    def deduplicate_items(self, items: list[ExhibitionItem]) -> list[ExhibitionItem]:
        return list(dict.fromkeys(items))

    async def save_to_json(
        self,
        filename: str,
        folder: str | Path | None = Path(__file__).parent.parent.parent.absolute() / "data" / "v2",
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
            this_folder = Path(__file__).parent.parent.parent.absolute() / "data" / prefix
            this_folder.mkdir(exist_ok=True)
        self.execution_time = execution_time

        if not (this_folder / f"{filename}.json").exists():
            (this_folder / f"{filename}.json").touch(exist_ok=True)

        async with aiofiles.open(this_folder / f"{filename}.json", mode="r+") as afp:
            context = await afp.read()
            if context:
                before_items = Exhibition.model_validate_json(context)
                last_week_update.set_before_items(before_items.items)

            await afp.seek(0)
            await afp.write(self.model_dump_json())
            await afp.truncate()
            last_week_update.set_after_items(self.items)

    async def save_to_rss(self) -> pathlib.Path:
        runtime_setting = get_settings()
        fg = FeedGenerator()

        fg.generator(generator="")
        fg.title(f"{self.information.fullname} 展覽列表")
        fg.link(href=self.information.external_link, rel="alternate")
        fg.description(f"收錄來自 {self.information.fullname} 的最新展覽資訊")
        fg.language("zh-TW")
        fg.lastBuildDate(get_datetime_now())

        for item in self.items:
            fe = fg.add_entry()
            fe.id(item.UUID)
            fe.title(f"{item.title}")
            fe.link(href=item.source_url)
            description_txt = []
            if item.date:
                description_txt.append(f"日期：{item.date}")
            if item.address:
                description_txt.append(f"地址：{item.address}")

            if item.tags:
                description_txt.append(f"標籤：{', '.join(item.tags)}")

            if item.figure:
                description_txt.append(f'<img src="{item.figure}" />')

            description = ("<br/>".join(description_txt) + "<br/>") if description_txt else ""

            fe.description(description)

            start_date = item.extract_start_date()
            if start_date:
                fe.pubDate(start_date.replace(tzinfo=get_timezone()))

            if item.figure:
                fe.enclosure(item.figure, 0, "image/jpeg")

        this_folder = Path(__file__).parent.parent.parent.absolute() / "data"
        file_path = this_folder / "rss" / f"{self.information.code_name}.xml"
        fg.rss_file(str(file_path), pretty=runtime_setting.IS_DEBUG)
        return file_path

    async def save_to_ics(self):
        cal = Calendar()
        cal.add("prodid", f"-//Been Been Play Project//{self.information.fullname}//TW")
        cal.add("version", "2.0")
        cal.add("x-wr-calname", f"{self.information.fullname} 展覽時程")
        cal.add("x-wr-timezone", get_timezone_str())

        for item in self.items:
            start_date = item.extract_start_date()
            end_date = item.extract_end_date()
            if not start_date or not end_date:
                continue

            event = Event()
            event.add("uid", item.UUID)  # 保持 UID 一致，更新時日曆才不會重複
            event.add("summary", f"[{self.information.fullname}] {item.title}")

            event.add("dtstart", start_date.date())
            event.add("dtend", end_date.date())

            description = f"展覽日期：{item.date}\n"
            if item.address:
                description += f"地點：{item.address}\n"
            if item.source_url:
                description += f"原始連結：{item.source_url}\n"
            if item.tags:
                description += f"標籤：{', '.join(item.tags)}"

            event.add("description", description)
            if item.address:
                event.add("location", item.address)
            event.add("dtstamp", get_datetime_now())
            cal.add_component(event)
        this_folder = Path(__file__).parent.parent.parent.absolute() / "data" / "ics"
        this_folder.mkdir(parents=True, exist_ok=True)
        file_path = this_folder / f"{self.information.code_name}.ics"
        async with aiofiles.open(file_path, mode="wb") as afp:
            await afp.write(cal.to_ical())
        return file_path


class LastWeekUpdateData(BaseModel):
    updated: datetime.datetime | None = Field(default_factory=get_datetime_now)
    items: list[ExhibitionItem] | None = Field(default_factory=list)

    def update_datetime(self):
        self.updated = get_datetime_now()


LAST_WEEK_FILE_PATH = Path(__file__).parent.parent.parent / "data" / "v2" / "last_week_update.json"


class LastWeekUpdate:
    def __init__(self):
        self.before_items: list["ExhibitionItem"] = []
        self.after_items: list["ExhibitionItem"] = []

    def set_before_items(self, items: list["ExhibitionItem"]):
        self.before_items.extend(items)

    def set_after_items(self, items: list["ExhibitionItem"]):
        self.after_items.extend(items)

    def get_last_week_update_items(self) -> set["ExhibitionItem"]:
        return set(self.after_items) - set(self.before_items)

    async def set_last_week_items(self):
        data = LastWeekUpdateData()

        if LAST_WEEK_FILE_PATH.exists():
            async with aiofiles.open(LAST_WEEK_FILE_PATH, "r") as afp:
                content = await afp.read()
                if content:
                    data = LastWeekUpdateData.model_validate_json(content)

        if data.updated is not None:
            today = get_datetime_now()
            if today.isocalendar()[:2] != data.updated.isocalendar()[:2]:
                data = LastWeekUpdateData()

        last_week_update_items = self.get_last_week_update_items()
        if last_week_update_items:
            data.items.extend(list(last_week_update_items))
            data.update_datetime()

        async with aiofiles.open(LAST_WEEK_FILE_PATH, "w+") as afp:
            await afp.write(data.model_dump_json(indent=2))


last_week_update = LastWeekUpdate()
