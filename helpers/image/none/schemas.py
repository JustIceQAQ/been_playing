from pydantic import BaseModel, Field


class Data(BaseModel):
    webp_link: str | None = Field(default=None)


class UploadResponse(BaseModel):
    success: bool | None = Field(default=False)
    status: int | None = Field(default=None)
    data: Data | None = Field(default=None)
