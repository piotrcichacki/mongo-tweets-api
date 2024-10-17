import json
from typing import List

from mongo_tweets_api.lib.mongo.client import create_mongo_client


def load_json(filepath: str) -> List[dict]:
    with open(filepath, "r") as json_file:
        data = json.load(json_file)
    return data


if __name__ == "__main__":
    mongo_client = create_mongo_client()
    tweets = load_json("../data/tweets.json")
    mongo_client.insert_many(tweets)
