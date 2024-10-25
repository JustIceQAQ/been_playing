from pydantic import BaseModel, Field, model_validator


class Data(BaseModel):
    id_: str | None = Field(alias="id", default=None)
    link: str | None = Field(default=None)
    webp_link: str | None = Field(default=None)
    error: str | None = Field(default=None)

    @model_validator(mode="after")
    def generate_webp_link(cls, values):
        if values.id_ is not None:
            values.webp_link = f"https://i.imgur.com/{values.id_}.webp"
        return values


class UploadResponse(BaseModel):
    success: bool
    status: int
    data: Data
