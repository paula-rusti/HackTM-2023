# TODO save the data read from the queue to a capped collection in MongoDB
import asyncio
from datetime import datetime

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient


class MongoClient:
    def __init__(
        self,
        host="localhost",
        port=27017,
        db_name="sensor_data_db",
    ):
        self.collection = None  # collection object, initialized in create_collection which is async
        self.client = AsyncIOMotorClient(host, port)
        self.db = self.client[db_name]

    async def create_collection(self, collection_name="sensor_data", capped=True, size=1000000):
        try:
            await self.db.create_collection(
                collection_name, capped=capped, size=size
            )
            self.collection = self.db["sensor_data"]
        except pymongo.errors.CollectionInvalid:
            self.collection = self.db["sensor_data"]
            print("Collection already exists")

    async def insert_one(self, document):
        # document["timestamp"] = datetime.utcnow()
        await self.collection.insert_one(document)


async def test_mongo_client():
    mongo_client_instance = MongoClient()
    await mongo_client_instance.create_collection()
    await mongo_client_instance.insert_one({"test": "test"})


if __name__ == '__main__':
    mongo_client_instance = MongoClient()
    asyncio.run(test_mongo_client())