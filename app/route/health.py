from fastapi import APIRouter
from starlette.responses import Response
from starlette.status import HTTP_200_OK

health_router = APIRouter(tags=["Health"])


@health_router.get("/health_check")
async def health_check() -> Response:
    return Response(status_code=HTTP_200_OK)
