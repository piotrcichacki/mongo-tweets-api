from typing import List, Any

from fastapi import APIRouter, Path, HTTPException, Query, Body, status, Depends
from typing_extensions import Annotated

from mongo_tweets_api.common.dependencies import create_mongo_repository_dependency
from mongo_tweets_api.lib.exceptions import TweetAlreadyExistsException
from mongo_tweets_api.lib.schema import Tweet, TweetUpdate
from mongo_tweets_api.mongo.repository import MongoDBRepository

router = APIRouter(
    prefix="/api/v1/tweets",
    tags=["tweets"]
)


@router.get(
    path="/",
    description="List existing tweets",
    response_model=List[Tweet],
    tags=["get"],
)
async def get_tweets(
    repository: Annotated[MongoDBRepository, Depends(create_mongo_repository_dependency)],
    skip: Annotated[int, Query(description="The number of tweets to omit when returning the results", ge=0)] = 0,
    limit: Annotated[int, Query(description="The maximum number of tweets to return", ge=0)] = 10,
) -> Any:
    return repository.get_tweets(skip=skip, limit=limit)


@router.get(
    path="/{tweet_id}",
    description="Get tweet by its identifier",
    response_model=Tweet,
    tags=["get"],
)
async def get_tweet_by_id(
    tweet_id: Annotated[str, Path(description="Tweet identifier")],
    repository: Annotated[MongoDBRepository, Depends(create_mongo_repository_dependency)],
) -> Any:
    tweet = repository.get_tweet_by_id(tweet_id)
    if not tweet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found")
    return tweet


@router.post(
    path="/",
    description="Create new tweet",
    status_code=status.HTTP_201_CREATED,
    tags=["create"],
)
async def create_tweet(
    tweet: Annotated[Tweet, Body(description="Tweet body")],
    repository: Annotated[MongoDBRepository, Depends(create_mongo_repository_dependency)],
) -> bool:
    try:
        return repository.insert_tweet(tweet.model_dump())
    except TweetAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tweet already exists")


@router.put(
    path="/{tweet_id}",
    description="Update existing tweet",
    tags=["update"],
)
async def update_tweet(
    tweet_id: Annotated[str, Path(description="Tweet identifier")],
    tweet: Annotated[Tweet, Body(description="Updated tweet")],
    repository: Annotated[MongoDBRepository, Depends(create_mongo_repository_dependency)],
) -> bool:
    return repository.replace_tweet_by_id(tweet_id, tweet.model_dump())


@router.patch(
    path="/{tweet_id}",
    description="Update existing tweet text",
    tags=["update"],
)
async def update_tweet_text(
    tweet_id: Annotated[str, Path(description="Tweet identifier")],
    tweet: Annotated[TweetUpdate, Body(description="Updated tweet text")],
    repository: Annotated[MongoDBRepository, Depends(create_mongo_repository_dependency)],
) -> bool:
    return repository.update_tweet_by_id(tweet_id, tweet.model_dump())


@router.delete(
    path="/{tweet_id}",
    description="Delete existing tweet",
    tags=["delete"],
)
async def delete_tweet(
    tweet_id: Annotated[str, Path(description="Tweet identifier")],
    repository: Annotated[MongoDBRepository, Depends(create_mongo_repository_dependency)],
) -> bool:
    return repository.delete_tweet_by_id(tweet_id)
