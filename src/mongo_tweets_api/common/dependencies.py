from mongo_tweets_api.mongo.client import create_mongo_client
from mongo_tweets_api.mongo.repository import create_mongo_repository


def create_mongo_repository_dependency():
    client = create_mongo_client(
        host="mongo",  # container name
        port=27017,
        username="root",
        password="example",
        database="service",
        collection="tweets",
    )
    return create_mongo_repository(client)
