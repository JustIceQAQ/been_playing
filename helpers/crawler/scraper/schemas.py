from enum import Enum

from pydantic import BaseModel, Field, model_validator


class Response(BaseModel):
    headers: dict = Field(default_factory=dict)
    body: str = Field()
    status_code: int = Field(alias="statusCode")


class JobStatus(str, Enum):
    Running = "running"
    Finished = "finished"


class ScraperResponse(BaseModel):
    status: JobStatus = Field(description="執行狀態", default=JobStatus.Running)
    is_finished: bool | None = Field(default=None)
    is_running: bool | None = Field(default=None)
    status_url: str | None = Field(
        description="執行狀態 url", alias="statusUrl", default=None
    )
    url: str | None = Field(default=None)
    response: Response | None = Field(default=None)
    status_code: int = Field()

    @model_validator(mode="after")
    def generate_webp_link(cls, values):
        values.is_running = values.status != JobStatus.Finished
        values.is_finished = values.status == JobStatus.Finished
        return values
