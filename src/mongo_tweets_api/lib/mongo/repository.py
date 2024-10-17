from dataclasses import dataclass
from typing import List

from mongo_tweets_api.lib.mongo.client import MongoDBClient


@dataclass
class MongoDBRepository:
    client: MongoDBClient

    # GET /tweets
    def get_tweets(self) -> List[dict]:
        return self.client.get_many({})

    # GET /tweets/{tweet_id}
    def get_tweet_by_id(self, tweet_id: str) -> dict:
        return self.client.get({"id": tweet_id})

    # GET /author/{author_id}/tweets
    def get_author_tweets(self, author_id: str) -> List[dict]:
        return self.client.get_many({"author_id": author_id})

    # GET /author/{author_id}/tweets/{tweet_id}
    def get_author_tweet_by_id(self, author_id: str, tweet_id: str) -> dict:
        return self.client.get({"$and": [{"author_id": author_id}, {"id": tweet_id}]})

    # POST /tweets/{tweet_id}
    def insert_tweet(self, data: dict) -> bool:
        return self.client.insert(data)

    # PATCH /tweets/{tweet_id}
    def update_tweet(self, tweet_id: str, data: dict) -> bool:
        return self.client.update({"id": tweet_id}, data)

    # PUT /tweets/{tweet_id}
    def upsert_tweet(self, tweet_id: str, data: dict) -> bool:
        return self.client.upsert({"id": tweet_id}, data)

    # DELETE /tweets/{tweet_id}
    def delete_tweet_by_id(self, tweet_id: str) -> bool:
        return self.client.delete({"id": tweet_id})


def create_mongo_repository(client: MongoDBClient) -> MongoDBRepository:
    return MongoDBRepository(client)
