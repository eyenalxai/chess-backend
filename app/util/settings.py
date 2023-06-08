from pydantic import BaseSettings, Field


class ApiSettings(BaseSettings):
    port: int | None = Field(..., env="PORT")
    allowed_origin: str = Field(..., env="ALLOWED_ORIGIN")
    is_local: bool = Field(env="IS_LOCAL", default=True)


api_settings = ApiSettings()
