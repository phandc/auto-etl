import logging
from .mongo_connector import mongo_connector, create_mongo_index

__logger__ = logging.getLogger(__name__)


async def init_config(config):
    await _init_mongo_client(config)

async def _init_mongo_client(config):
    try:
        
        mongo_connector.connect(config.MONGO_URI)

        client = mongo_connector.get_client()

        
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

    except Exception as e:
        print(f"Error :", e)

    create_mongo_index()