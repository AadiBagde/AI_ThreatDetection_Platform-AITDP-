from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ingestion_service.app.core import paths  # noqa: F401
from ingestion_service.app.core.config import get_settings
from ingestion_service.app.core.logging import get_logger, setup_logging
from ingestion_service.app.middleware.request_logging import RequestLoggingMiddleware
from ingestion_service.app.routes import health, ingest

error_logger = get_logger("error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    setup_logging(settings.log_level)
    ingestion_logger = get_logger("ingestion")
    ingestion_logger.info(
        "Starting %s v%s", settings.app_name, settings.app_version
    )
    yield
    ingestion_logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging(settings.log_level)
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AITDP network packet ingestion API (Phase 1)",
        lifespan=lifespan,
    )

    app.add_middleware(RequestLoggingMiddleware)
    app.include_router(health.router)
    app.include_router(ingest.router)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        error_logger.warning(
            "Validation error on %s %s: %s",
            request.method,
            request.url.path,
            exc.errors(),
        )
        return JSONResponse(
            status_code=422,
            content={"detail": jsonable_encoder(exc.errors())},
        )

    return app


app = create_app()
