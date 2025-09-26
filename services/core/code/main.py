from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.core.code.api.routers import main_router
from services.core.code.core.config import settings
from services.core.code.logging_config import setup_logging


listener = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    listener.start()
    yield
    listener.stop()

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
)

app.include_router(main_router)
