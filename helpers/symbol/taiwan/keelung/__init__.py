from enum import Enum

from helpers.storage.location import Name, Location
from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class KeelungCity(Enum):
    CITY = Name(name="基隆市", code="10017000", ios3166ma=ISO3166Ma.KEELUNG_CITY)

    @property
    def city(self) -> Location:
        return Location(city=self.value)

    @property
    def zhong_zheng_10017010(self) -> Location:
        return Location(city=self.value, area=Name(name="中正區", code="10017010"))

    @property
    def qi_du_10017020(self) -> Location:
        return Location(city=self.value, area=Name(name="七堵區", code="10017020"))

    @property
    def nuan_nuan_10017030(self) -> Location:
        return Location(city=self.value, area=Name(name="暖暖區", code="10017030"))

    @property
    def ren_ai_10017040(self) -> Location:
        return Location(city=self.value, area=Name(name="仁愛區", code="10017040"))

    @property
    def zhong_shan_10017050(self) -> Location:
        return Location(city=self.value, area=Name(name="中山區", code="10017050"))

    @property
    def an_le_10017060(self) -> Location:
        return Location(city=self.value, area=Name(name="安樂區", code="10017060"))

    @property
    def xin_yi_10017070(self) -> Location:
        return Location(city=self.value, area=Name(name="信義區", code="10017070"))
