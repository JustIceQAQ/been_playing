from typing import Any

from pydantic import BaseModel, Field


class TwTcResponse(BaseModel):
    year: int
    text: str
    parsed: Any | None = Field(default=None)
    items: list[Any] = Field(default_factory=list)
