from contextlib import asynccontextmanager
from typing import AsyncGenerator
import redis.asyncio
from fastapi import FastAPI

from app.logger import service_logger
from app.common.utils.env_validator import settings
from app.containers import AppContainers
from app.ormconfig import DatabaseLoader

# Endpoints
from app.hello.endpoints import router as hello_router
from app.auth.endpoints import router as auth_router
from app.kiosk.endpoints import router as kiosk_router

# Redis OM Models
from app.kiosk.session import KioskLoginSession

logger = service_logger("bootstrapper")


def bootstrap() -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
        logger.info("Starting application")

        application.container = container

        container.wire(
            modules=[
                __name__,
                "app.hello.endpoints",
                "app.auth.endpoints",
                "app.kiosk.endpoints",
            ]
        )
        logger.info("Container Wiring complete")

        redis_connection = redis.asyncio.Redis.from_url(
            settings.REDIS_URI, encoding="utf8", decode_responses=True
        )

        KioskLoginSession.Meta.database = redis_connection
        logger.info("Redis OM database connection established")

        async with DatabaseLoader.load(application):
            logger.info("Tortoise ORM registered")
            yield

        await redis_connection.close()
        logger.info("Redis connections closed")
        logger.info("Shutting down application")
        logger.info("Tortoise ORM connections closed")
        logger.info("Application shutdown complete")

    app = FastAPI(
        title="TableTurn API",
        lifespan=lifespan,
        redoc_url=None,
        debug=settings.APP_ENV == "development",
    )

    # startup 이벤트 제거됨 - lifespan으로 이동

    return app


container = AppContainers()
server = bootstrap()

server.include_router(auth_router)
server.include_router(hello_router)
server.include_router(kiosk_router)
