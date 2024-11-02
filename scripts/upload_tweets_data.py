import json
from typing import List

from mongo_tweets_api.lib.mongo.client import create_mongo_client


def load_json(filepath: str) -> List[dict]:
    with open(filepath, "r") as json_file:
        data = json.load(json_file)
    return data


def set_id_to_mongo_collection_id(tweet: dict) -> dict:
    tweet["_id"] = tweet.pop("id")
    return tweet


if __name__ == "__main__":
    mongo_client = create_mongo_client()
    tweets = load_json("../data/tweets.json")
    tweets = [set_id_to_mongo_collection_id(tweet) for tweet in tweets]
    mongo_client.insert_many(tweets)
