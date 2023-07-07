from motor.motor_asyncio import AsyncIOMotorClient


class MongoConnector():
    _client = AsyncIOMotorClient

    def connect(self, uri: str):
        self._client = AsyncIOMotorClient(uri)

    def get_client(self):
        return self._client


mongo_connector = MongoConnector()


def create_mongo_index():
    pass
