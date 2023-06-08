from pydantic import BaseSettings, Field


class ApiSettings(BaseSettings):
    port: int | None = Field(..., env="PORT")
    allowed_origin: str = Field(..., env="ALLOWED_ORIGIN")


api_settings = ApiSettings()
