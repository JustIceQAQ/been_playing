from enum import Enum

from helpers.storage.location import Location, Name
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class KeelungCity(Enum):
    CITY = Name(name="基隆市", code="10017000", ios3166ma=ISO3166Ma.KEELUNG_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def zhongzheng_10017010(self) -> Location:
        return Location(city=self.value, area=Name(name="中正區", code="10017010"))

    @property
    def qidu_10017020(self) -> Location:
        return Location(city=self.value, area=Name(name="七堵區", code="10017020"))

    @property
    def nuannuan_10017030(self) -> Location:
        return Location(city=self.value, area=Name(name="暖暖區", code="10017030"))

    @property
    def renai_10017040(self) -> Location:
        return Location(city=self.value, area=Name(name="仁愛區", code="10017040"))

    @property
    def zhongshan_10017050(self) -> Location:
        return Location(city=self.value, area=Name(name="中山區", code="10017050"))

    @property
    def anle_10017060(self) -> Location:
        return Location(city=self.value, area=Name(name="安樂區", code="10017060"))

    @property
    def xinyi_10017070(self) -> Location:
        return Location(city=self.value, area=Name(name="信義區", code="10017070"))
