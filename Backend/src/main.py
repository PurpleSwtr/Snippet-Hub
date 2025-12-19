from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache

from src.core.db import Base, engine

from redis.asyncio import Redis
from fastapi_cache.backends.redis import RedisBackend

from src.ollama.router import router as ollama_router
from src.snippets.router import router as options_router
from src.icons.router import router as icons_router

from src.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:

    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db.cache
    )
    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix
        # namespace=settings.cache.namespace.icons_list,
    )
    Base.metadata.create_all(engine)
    print("Таблицы созданы")
    yield

app = FastAPI(
    title="LLM Manager",
    root_path="/api/v1",
    lifespan=lifespan 
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ollama_router)
app.include_router(options_router)
app.include_router(icons_router)

app.mount("/static/icons", StaticFiles(directory=settings.FRONT_STATIC_DIR), name="icons")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         app, 
#         host="0.0.0.0", 
#         port=8000,
#         log_level="info"
#     )