import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from ml_engine.app.core.logging import get_logger

request_logger = get_logger("request")
error_logger = get_logger("error")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        request_logger.info("%s %s", request.method, request.url.path)

        try:
            response = await call_next(request)
        except Exception:
            error_logger.exception(
                "Unhandled error for %s %s", request.method, request.url.path
            )
            raise

        duration_ms = (time.perf_counter() - start) * 1000
        request_logger.info(
            "%s %s -> %s (%.2f ms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
