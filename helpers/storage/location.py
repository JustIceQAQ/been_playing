from pydantic import BaseModel, Field


class Name(BaseModel):
    name: str = Field(description="名稱")
    code: str = Field(description="代號")
    ios3166ma: str | None = Field(default=None, description="IOS 3166 / MA 代號")


class Location(BaseModel):
    city: Name = Field(description="縣/市")
    area: Name | None = Field(description="區域", default=None)
