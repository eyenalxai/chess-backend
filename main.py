import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.route.chess import chess_router
from app.util.settings import api_settings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[api_settings.allowed_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chess_router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=api_settings.port,
        proxy_headers=True,
    )
