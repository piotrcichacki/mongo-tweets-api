from dataclasses import dataclass
from typing import List, Optional

from pymongo import MongoClient
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database


@dataclass
class MongoDBClient:
    _client = MongoClient
    database: str
    collection: str
    _projection: Optional[dict] = None

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str,
        collection: str,
        include: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None
    ) -> None:
        self._client = MongoClient(
            host=host,
            port=port,
            username=username,
            password=password,
        )
        self.database_name = database
        self.collection_name = collection
        self._projection = self.create_projection(include, exclude)

    @staticmethod
    def create_projection(include: Optional[List[str]] = None, exclude: Optional[List[str]] = None) -> Optional[dict]:
        _projection = {}
        if include:
            _projection.update({field: 1 for field in include})
        if exclude:
            _projection.update({field: 0 for field in exclude})
        if _projection:
            return _projection

    @property
    def projection(self) -> Optional[dict]:
        return self._projection

    @property
    def database(self) -> Database:
        return self._client[self.database_name]

    @property
    def collection(self) -> Collection:
        return self._client[self.database_name][self.collection_name]

    def insert(self, data: dict) -> bool:
        response = self.collection.insert_one(data)
        return response.acknowledged

    def insert_many(self, data: List[dict]) -> bool:
        response = self.collection.insert_many(data)
        return response.acknowledged

    def update(self, query: dict, value: dict) -> bool:
        response = self.collection.update_one(query, {"$set": value}, upsert=False)
        return response.acknowledged

    def upsert(self, query: dict, value: dict) -> bool:
        response = self.collection.update_one(query, {"$set": value}, upsert=True)
        return response.acknowledged

    def get(self, query: dict) -> dict:
        return self.collection.find_one(query, self.projection)

    def get_many(self, query: dict) -> List[dict]:
        return [document for document in self.collection.find(query, self.projection)]

    def delete(self, query: dict) -> bool:
        response = self.collection.delete_one(query)
        return response.acknowledged

    def delete_many(self, query: dict) -> bool:
        response = self.collection.delete_many(query)
        return response.acknowledged


def create_mongo_client() -> MongoDBClient:
    return MongoDBClient(
        host="localhost",
        port=27017,
        username="root",
        password="example",
        database="service",
        collection="tweets",
    )
