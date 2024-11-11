from typing import List

import pymongo

from mongo_tweets_api.mongo.client import MongoDBClient, create_mongo_client


def get_author_tweets_text(client: MongoDBClient, author_id: str) -> List[dict]:
    query = {"author_id": author_id}
    projection = {"_id": 0, "text": 1}
    return [document for document in client.collection.find(query, projection)]


def get_author_tweets_count(client: MongoDBClient, author_id: str) -> int:
    query = {"author_id": author_id}
    return client.collection.count_documents(query)


def get_author_most_liked_tweet(client: MongoDBClient, author_id: str) -> dict:
    query = {"author_id": author_id}
    return client.collection.find(query).sort({"public_metrics.like_count": pymongo.DESCENDING}).next()


def get_tweets_with_username_mention(client: MongoDBClient, username: str) -> List[dict]:
    query = {"entities.mentions": {"$elemMatch": {"username": username}}}
    return [document for document in client.collection.find(query)]


def aggregate_authors_tweets_public_metrics_to_new_collection(client: MongoDBClient, lang: str) -> None:
    pipeline = [
        {"$match": {"lang": lang}},
        {"$group": {
            "_id": "$author_id",
            "like_sum": {"$sum": "$public_metrics.like_count"},
            "quote_sum": {"$sum": "$public_metrics.quote_count"},
            "reply_sum": {"$sum": "$public_metrics.reply_count"},
            "retweet_sum": {"$sum": "$public_metrics.retweet_count"},
            "bookmark_sum": {"$sum": "$public_metrics.bookmark_count"},
            "impression_sum": {"$sum": "$public_metrics.impression_count"}
        }},
        {"$out": {"db": client.database_name, "coll": "authors"}}
    ]
    client.collection.aggregate(pipeline)


if __name__ == "__main__":
    mongo_client = create_mongo_client(
        host="localhost",
        port=27017,
        username="root",
        password="example",
        database="service",
        collection="tweets",
    )

    response = get_author_tweets_text(client=mongo_client, author_id="2302131097")
    # response = get_author_tweets_count(client=mongo_client, author_id="2302131097")
    # response = get_author_most_liked_tweet(client=mongo_client, author_id="2302131097")
    # response = get_tweets_with_username_mention(client=mongo_client, username="__Lewica")
    # aggregate_authors_tweets_public_metrics_to_new_collection(client=mongo_client, lang="pl")

    print(response)
