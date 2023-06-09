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
                "https://{frontend_domain}".format(frontend_domain=self.allowed_origin)
            ]
        return ["http://{frontend_domain}".format(frontend_domain=self.allowed_origin)]


api_settings = ApiSettings()
