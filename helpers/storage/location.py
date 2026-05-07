from pydantic import BaseModel, Field

from helpers.symbol.taiwan.iso_3166_ma import ISO3166Ma


class Name(BaseModel):
    name: str = Field(description="名稱")
    code: str = Field(description="代號")
    ios3166ma: str | ISO3166Ma | None = Field(default=None, description="IOS 3166 / MA 代號")


class Location(BaseModel):
    city: Name
    area: Name | None = None
