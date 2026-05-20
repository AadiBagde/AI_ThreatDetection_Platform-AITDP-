from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ml_engine.app.core import paths  # noqa: F401
from ml_engine.app.core.config import get_settings
from ml_engine.app.core.logging import get_logger, setup_logging
from ml_engine.app.loaders.model_loader import ModelLoadError, load_models
from ml_engine.app.middleware.request_logging import RequestLoggingMiddleware
from ml_engine.app.routes import health, predict
from ml_engine.app.services.prediction_logger import log_malformed_features, log_model_loaded

error_logger = get_logger("error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    setup_logging(settings.log_level)
    prediction_log = get_logger("prediction")

    try:
        artifacts = load_models()
        log_model_loaded(
            model_version=artifacts.metadata.get("model_version", "unknown"),
            model_type=artifacts.metadata.get("model_type", "unknown"),
            accuracy=artifacts.metadata.get("test_accuracy"),
        )
        prediction_log.info(
            "Starting %s v%s | models loaded from %s",
            settings.app_name,
            settings.app_version,
            artifacts.model_dir,
        )
    except ModelLoadError as exc:
        error_logger.error("Model loading failed at startup: %s", exc)

    yield
    prediction_log.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AITDP ML threat detection microservice (Phase 3)",
        lifespan=lifespan,
    )

    app.add_middleware(RequestLoggingMiddleware)
    app.include_router(health.router)
    app.include_router(predict.router)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        log_malformed_features(exc.errors())
        error_logger.warning(
            "Validation error on %s %s", request.method, request.url.path
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
