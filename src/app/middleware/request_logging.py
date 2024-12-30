from typing import Callable

from log import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        logger.info(
            {
                "method": request.method,
                "url": request.url,
                "status_code": response.status_code,
                "remote_ip": request.headers.get(
                    "X-Forwarded-For", request.client.host
                ),
            }
        )

        return response
