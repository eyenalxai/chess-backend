from pydantic import BaseSettings, Field


class ApiSettings(BaseSettings):
    port: int = Field(env="PORT", default=8000)
    allowed_origin: str = Field(..., env="ALLOWED_ORIGIN")
    is_local: bool = Field(env="IS_LOCAL", default=True)
    api_workers: int = Field(env="API_WORKERS", default=4)

    @property
    def allowed_origins(self: "ApiSettings") -> list[str]:
        if not self.is_local:
            return [
                "https://{allowed_origin}".format(allowed_origin=self.allowed_origin)
            ]
        return ["http://{allowed_origin}".format(allowed_origin=self.allowed_origin)]


api_settings = ApiSettings()  # type: ignore
