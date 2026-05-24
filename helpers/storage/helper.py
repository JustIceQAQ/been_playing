import datetime
import pathlib
import re
import uuid
from decimal import Decimal
from pathlib import Path

import aiofiles
from pydantic import BaseModel, Field, model_validator
from feedgen.feed import FeedGenerator
from icalendar import Calendar, Event
from configs.settings import get_settings
from helpers.storage.coordinate import Coordinate
from helpers.storage.location import Location
from helpers.storage.social_media import SocialMedia
from helpers.symbol.venue import VenueType
from helpers.utils_helper import (
    get_date,
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
    source_url: str
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
                return datetime.datetime.strptime(match.group(1), "%Y-%m-%d").replace(tzinfo=get_date.timezone)
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
                return datetime.datetime.strptime(this_date, "%Y-%m-%d").replace(tzinfo=get_date.timezone)
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

    def _sort_key(self) -> tuple:
        today = get_date.time_now.replace(hour=0, minute=0, second=0, microsecond=0)
        MAX_DATE = datetime.datetime(9999, 12, 31, tzinfo=get_date.timezone)

        start = self.extract_start_date()
        end = self.extract_end_date()
        date_type = self.extract_date_type()

        # 進行中（無結束日期）
        if date_type == 3:
            return (0, 1, start or MAX_DATE)

        # 進行中 / 尚未開始 / 已結束（有完整範圍）
        if date_type == 0 and start and end:
            if start <= today <= end:
                return (0, 0, end)  # 進行中，以結束日期 asc 排序
            elif start > today:
                return (1, 0, start)  # 尚未開始（範圍型），以開始日期 asc 排序
            else:
                return (3, 0, end)  # 已結束

        # 尚未開始 / 已結束（單一日期）
        if date_type == 1 and start:
            if start > today:
                return (1, 1, start)  # 尚未開始（單一日期）
            elif today > start:
                return (3, 1, start)  # 已結束（單一日期）
            else:
                return (0, 1, MAX_DATE)  # 今天即為展期

        # 無法判斷
        return (2, self.count_none_fields(), MAX_DATE)

    def __lt__(self, other: "ExhibitionItem") -> bool:
        return self._sort_key() < other._sort_key()

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


class Information(BaseModel):
    fullname: str = Field(description="名稱")
    code_name: str = Field(description="代號")
    external_link: str = Field(description="外部連結")
    profile_image_url: str | None = Field(default=None, description="場館形象照")

    branch_coordinates: Coordinate | list[Coordinate] | None = Field(default=None, description="地理資訊")
    location_code: Location | None = Field(default=None, description="經緯度，(舊)")
    venue_type: VenueType | None = Field(default=None, description="場所類型")

    has_rss: bool | None = Field(default=False, description="是否有RSS")
    has_ics: bool | None = Field(default=False, description="是否有ICS")


class Exhibition(BaseModel):
    information: Information
    counts: int = 0
    items: list[ExhibitionItem] = Field(default_factory=list)
    social_media: SocialMedia | None = Field(default=None, description="社群媒體")
    last_update: str = Field(default_factory=lambda: get_date.now_format_to_ios)
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
        folder: Path = Path(__file__).parent.parent.parent.absolute() / "data" / "v2",
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

        this_folder = (
            Path(this_folder)
            if this_folder is not None
            else Path(__file__).parent.parent.parent.absolute() / "data" / "v2"
        )

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

        if execution_time is not None:
            execution_stats.record(
                code_name=self.information.code_name,
                fullname=self.information.fullname,
                execution_time=execution_time,
                last_update=self.last_update,
            )

    async def save_to_rss(self) -> pathlib.Path:
        runtime_setting = get_settings()
        fg = FeedGenerator()

        fg.generator(generator="")
        fg.title(f"{self.information.fullname} 展覽列表")
        fg.link(href=self.information.external_link, rel="alternate")
        fg.description(f"收錄來自 {self.information.fullname} 的最新展覽資訊")
        fg.language("zh-TW")
        fg.lastBuildDate(get_date.time_now)

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
                fe.pubDate(start_date.replace(tzinfo=get_date.timezone))

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
        cal.add("x-wr-timezone", get_date.timezone_string)

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
            event.add("dtstamp", get_date.time_now)
            cal.add_component(event)
        this_folder = Path(__file__).parent.parent.parent.absolute() / "data" / "ics"
        this_folder.mkdir(parents=True, exist_ok=True)
        file_path = this_folder / f"{self.information.code_name}.ics"
        async with aiofiles.open(file_path, mode="wb") as afp:
            await afp.write(cal.to_ical())
        return file_path


class LastWeekUpdateData(BaseModel):
    updated: datetime.datetime = Field(default_factory=lambda: get_date.time_now)
    items: list[ExhibitionItem] = Field(default_factory=list)

    def update_datetime(self):
        self.updated = get_date.time_now


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
            today = get_date.time_now
            if today.isocalendar()[:2] != data.updated.isocalendar()[:2]:
                data = LastWeekUpdateData()

        last_week_update_items = self.get_last_week_update_items()
        if last_week_update_items:
            data.items.extend(list(last_week_update_items))
            data.update_datetime()

        async with aiofiles.open(LAST_WEEK_FILE_PATH, "w+") as afp:
            await afp.write(data.model_dump_json(indent=2))


last_week_update = LastWeekUpdate()


EXECUTION_STATS_FILE_PATH = Path(__file__).parent.parent.parent / "data" / "v2" / "_EXECUTION_STATS.json"


class ExecutionStatsItem(BaseModel):
    code_name: str
    fullname: str
    execution_time: float
    last_update: str


class ExecutionStatsData(BaseModel):
    generated_at: str = Field(default_factory=lambda: get_date.now_format_to_ios)
    runners: list[ExecutionStatsItem] = Field(default_factory=list)
    total_runners: int = 0
    total_execution_time: float = 0.0
    avg_execution_time: float = 0.0
    max_execution_time: float = 0.0
    min_execution_time: float = 0.0

    @model_validator(mode="after")
    def compute_summary(cls, values):
        times = [r.execution_time for r in values.runners]
        if times:
            values.total_runners = len(times)
            values.total_execution_time = round(sum(times), 4)
            values.avg_execution_time = round(sum(times) / len(times), 4)
            values.max_execution_time = round(max(times), 4)
            values.min_execution_time = round(min(times), 4)
        return values


class ExecutionStats:
    def __init__(self):
        self._records: list[ExecutionStatsItem] = []

    def record(self, code_name: str, fullname: str, execution_time: float, last_update: str):
        self._records.append(
            ExecutionStatsItem(
                code_name=code_name,
                fullname=fullname,
                execution_time=round(execution_time, 4),
                last_update=last_update,
            )
        )

    async def save(self):
        sorted_records = sorted(self._records, key=lambda r: r.execution_time, reverse=True)
        data = ExecutionStatsData(runners=sorted_records)
        async with aiofiles.open(EXECUTION_STATS_FILE_PATH, "w+") as afp:
            await afp.write(data.model_dump_json(indent=2))


execution_stats = ExecutionStats()
