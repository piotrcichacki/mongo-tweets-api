from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio.client import Redis

from mongo_tweets_api.routers import tweets


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    client = Redis(host="redis", port=6379)
    FastAPICache.init(RedisBackend(client), prefix="fastapi-cache")
    yield


app = FastAPI(
    title="Tweets Mongo API",
    summary="Tweets API based on mongo database",
    description="An API for working with tweet data based on mongo db, created as part of learning REST API and NoSQL.",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(tweets.router)


@app.get(
    path="/alert/ping",
    description="Used for liveness and readiness probes",
)
async def ping() -> str:
    return "pong"
