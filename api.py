import uvicorn

from app.util.settings import api_settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=api_settings.port,
        proxy_headers=True,
        workers=api_settings.api_workers,
    )
