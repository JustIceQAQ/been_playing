from pydantic import BaseModel, Field


class Data(BaseModel):
    webp_link: str | None = Field(default=None)


class UploadResponse(BaseModel):
    success: bool
    status: int
    data: Data
