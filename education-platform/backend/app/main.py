from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging, get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    logger.info("Starting %s", settings.APP_NAME)
    yield
    logger.info("Stopping %s", settings.APP_NAME)


def get_api_router() -> APIRouter | None:
    try:
        from app.api.v1.router import api_router
    except ImportError:
        logger.warning("API router is not ready yet; starting without routes")
        return None

    if not isinstance(api_router, APIRouter):
        logger.warning("api_router is not an APIRouter; starting without routes")
        return None

    return api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        version="0.1.0",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    api_router = get_api_router()
    if api_router is not None:
        app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, Any]:
        return {
            "status": "ok",
            "service": settings.APP_NAME,
            "environment": settings.APP_ENV,
        }

    return app


app = create_app()
