from fastapi import FastAPI

from mongo_tweets_api.routers import tweets

app = FastAPI(
    title="Tweets Mongo API",
    summary="Tweets API based on mongo database",
    description="An API for working with tweet data based on mongo db, created as part of learning REST API and NoSQL.",
    version="0.1.0",
)

app.include_router(tweets.router)


@app.get(
    path="/alert/ping",
    description="Used for liveness and readiness probes",
)
async def ping() -> str:
    return "pong"
