from dataclasses import dataclass
from typing import List

from pymongo.errors import DuplicateKeyError

from mongo_tweets_api.lib.exceptions import TweetAlreadyExistsException
from mongo_tweets_api.mongo.client import MongoDBClient


@dataclass
class MongoDBRepository:
    client: MongoDBClient

    def get_tweets(self, *args, **kwargs) -> List[dict]:
        tweets = self.client.get_many({}, *args, **kwargs)
        for tweet in tweets:
            tweet["id"] = tweet["_id"]
        return tweets

    def get_tweet_by_id(self, tweet_id: str) -> dict:
        tweet = self.client.get({"_id": tweet_id})
        if tweet:
            tweet["id"] = tweet["_id"]
        return tweet

    def insert_tweet(self, data: dict) -> bool:
        data["_id"] = data.pop("id")
        try:
            return self.client.insert(data)
        except DuplicateKeyError:
            raise TweetAlreadyExistsException()

    def replace_tweet_by_id(self, tweet_id: str, data: dict) -> bool:
        return self.client.upsert({"_id": tweet_id}, data)

    def update_tweet_by_id(self, tweet_id: str, data: dict) -> bool:
        return self.client.update({"_id": tweet_id}, data)

    def delete_tweet_by_id(self, tweet_id: str) -> bool:
        return self.client.delete({"_id": tweet_id})


def create_mongo_repository(client: MongoDBClient) -> MongoDBRepository:
    return MongoDBRepository(client)
