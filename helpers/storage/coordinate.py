import re
from _decimal import Decimal
from typing import Any, Self

from pydantic import BaseModel, Field, model_serializer, model_validator

from helpers.storage.location import Location


class GoogleMaps(BaseModel):
    """Google Maps"""

    plus_code: str | None = Field(default=None, description="Google Maps Plus Code")


class OpenStreetMapKeys(BaseModel):
    """Open Street Map Keys"""

    amenity: str | None = Field(default=None, description="用來描述給住民和訪客使用的重要設施")
    landuse: str | None = Field(
        default=None, description="Mainly used for describing the primary use of areas of land."
    )
    type: str | None = Field(default=None, description="Type of a relation.")
    tourism: str | None = Field(default=None, description="A place or object of specific interest to tourists.")
    museum: str | None = Field(default=None, description="Type of museum classified by topic.")
    air_conditioning: str | None = Field(default=None, description="Indication whether a feature has air-conditioning.")
    wheelchair: str | None = Field(default=None, description="Indicate if a special place can be used with wheelchairs")

    @model_serializer
    def serialize(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}


class OpenStreetMap(BaseModel):
    """Open Street Map"""

    osm_id: int | None = Field(default=None, description="OSM Node/Way/Relation ID")
    osm_type: str | None = Field(default=None, description="node / way / relation")
    osm_url: str | None = Field(default=None, description="完整 OSM URL")
    keys: OpenStreetMapKeys | None = Field(default=None, description="OpenStreetMap 設施語意")

    @model_validator(mode="after")
    def parse_from_url(self) -> Self:
        if self.osm_url and (self.osm_id is None or self.osm_type is None):
            pattern = r"openstreetmap\.org/(node|way|relation)/(\d+)"
            match = re.search(pattern, self.osm_url)
            if match:
                self.osm_type = match.group(1)
                self.osm_id = int(match.group(2))
            else:
                raise ValueError(f"無法從 URL 解析 osm_type / osm_id：{self.osm_url}")
        return self


class Wiki(BaseModel):
    wikidata: str | None = Field(default=None, description="Wikidata Q-ID，例如 Q699040")
    wikipedia: str | None = Field(default=None, description="Wikipedia 條目，例如 zh:台北當代藝術館")

    @property
    def wikidata_url(self) -> str | None:
        if self.wikidata:
            return f"https://www.wikidata.org/wiki/{self.wikidata}"
        return None

    @property
    def wikipedia_url(self) -> str | None:
        if self.wikipedia and ":" in self.wikipedia:
            lang, title = self.wikipedia.split(":", 1)
            return f"https://{lang}.wikipedia.org/wiki/{title.replace(' ', '_')}"
        return None


class GeoPoint(BaseModel):
    """經緯度座標"""

    longitude: Decimal | None = Field(default=None, description="經度")
    latitude: Decimal | None = Field(default=None, description="緯度")
    raw_coordinates: str | None = Field(default=None, description="原始經緯度字串，格式：緯度, 經度")

    @model_validator(mode="after")
    def parse_raw_coordinates(self) -> Self:
        if self.raw_coordinates and (self.latitude is None or self.longitude is None):
            try:
                parts = self.raw_coordinates.split(", ")
                if len(parts) == 2:
                    self.latitude = Decimal(parts[0].strip())
                    self.longitude = Decimal(parts[1].strip())
                else:
                    raise ValueError(f"格式錯誤，預期「緯度, 經度」：{self.raw_coordinates}")
            except Exception as e:
                raise ValueError(f"座標解析失敗: {e}")
        return self


class Coordinate(BaseModel):
    """地理資訊"""

    name: str | None = Field(default=None, description="名稱, 若為None 則代表該地點沒有分館")
    location_code: Location | None = Field(default=None, description="ISO 3166/MA")
    address: str | None = Field(description="完整地址", default=None)

    raw_coordinates: str | None = Field(default=None, description="原始經緯度字串，準備移除!")
    longitude: Decimal | None = Field(default=None, description="經度(舊)，準備移除!")
    latitude: Decimal | None = Field(default=None, description="緯度(舊)，準備移除!")
    geo_point: GeoPoint | None = Field(default=None, description="經緯度座標")
    open_street_map: OpenStreetMap | None = Field(default=None, description="OpenStreetMap(OSM) Information")
    wiki: Wiki | None = Field(default=None, description="WiKi Information")
    google_maps: GoogleMaps | None = Field(default=None, description="Google Maps Information")

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

    @model_validator(mode="after")
    def sync_geo_point(self) -> Self:
        if self.geo_point is None and self.longitude is not None and self.latitude is not None:
            self.geo_point = GeoPoint(
                longitude=self.longitude,
                latitude=self.latitude,
            )

        elif self.geo_point is not None and self.longitude is None and self.latitude is None:
            self.longitude = self.geo_point.longitude
            self.latitude = self.geo_point.latitude

        return self
