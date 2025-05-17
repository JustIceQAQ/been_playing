from pydantic import BaseModel, Field


class Response(BaseModel):
    body: str | dict


class ScrapeDoResponse(BaseModel):
    response: Response | None = Field(default=None)
    status_code: int
    is_success: bool
