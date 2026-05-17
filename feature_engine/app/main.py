from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from feature_engine.app.core import paths  # noqa: F401
from feature_engine.app.core.config import get_settings
from feature_engine.app.core.logging import get_logger, setup_logging
from feature_engine.app.middleware.request_logging import RequestLoggingMiddleware
from feature_engine.app.routes import extract, health

error_logger = get_logger("error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    setup_logging(settings.log_level)
    extraction_logger = get_logger("extraction")
    extraction_logger.info(
        "Starting %s v%s on port %s",
        settings.app_name,
        settings.app_version,
        settings.port,
    )
    yield
    extraction_logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AITDP feature extraction microservice (Phase 2)",
        lifespan=lifespan,
    )

    app.add_middleware(RequestLoggingMiddleware)
    app.include_router(health.router)
    app.include_router(extract.router)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        error_logger.warning(
            "Malformed packet / validation error on %s %s | errors=%s",
            request.method,
            request.url.path,
            exc.errors(),
        )
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "detail": jsonable_encoder(exc.errors()),
            },
        )

    return app


app = create_app()
