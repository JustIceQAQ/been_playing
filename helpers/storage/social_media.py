from pydantic import BaseModel, Field, model_serializer


class SocialMedia(BaseModel):
    """社群媒體"""

    facebook: str | None = Field(default=None, description="Facebook 連結")
    instagram: str | None = Field(default=None, description="Instagram 連結")
    youtube: str | None = Field(default=None, description="YouTube 連結")
    x: str | None = Field(default=None, description="X (Twitter) 連結")
    line: str | None = Field(default=None, description="LINE 官方帳號連結")
    threads: str | None = Field(default=None, description="Threads 連結")

    @model_serializer
    def serialize(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}
