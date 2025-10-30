import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

try:
    from fastapi_cache.backends.redis import RedisBackend
    from redis.asyncio import Redis
except ModuleNotFoundError: 
    Redis = None
    RedisBackend = None

from app.api import api_router
from app.core.config import settings
from app.core.db import create_database

logger = logging.getLogger(__name__)


async def init_cache() -> None:
    """Initialise caching backend with Redis when available."""
    backend = None

    if Redis and RedisBackend and settings.REDIS_URL:
        try:
            redis = Redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=False)
            await redis.ping()
            backend = RedisBackend(redis)
            logger.info("Connected to Redis cache backend.")
        except Exception: 
            logger.warning("Redis backend unavailable. Falling back to in-memory cache.", exc_info=True)

    if backend is None:
        backend = InMemoryBackend()
        logger.info("Using in-memory cache backend.")

    FastAPICache.init(backend, prefix=settings.CACHE_PREFIX)


def create_app() -> FastAPI:
    """Application factory."""
    logging.basicConfig(level=logging.INFO)
    app = FastAPI(title=settings.PROJECT_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def on_startup() -> None:
        create_database()
        await init_cache()

    @app.get("/health", tags=["health"])
    async def health() -> JSONResponse:
        return JSONResponse({"status": "ok"})

    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_app()
