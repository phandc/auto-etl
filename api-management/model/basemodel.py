import datetime
import logging

import pymongo
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from typing import Any
from pymongo.errors import DuplicateKeyError
from common.singleton import Singleton
from database.mongo_connector import mongo_connector

__logger__ = logging.getLogger()

TIME_FIELDS = [
    'last_received',
    'created_time',
    'updated_time',
    'time_received'
]


class MongoBaseModel(object, metaclass=Singleton):
    db: Any = None
    collection: Any = None

    def __init__(self, db, collection):
        self.db = mongo_connector.get_client()[db]
        self.collection = self.db[collection]

    def convert_fields(self, item):
        try:
            _id = item.pop('_id', None)
            if _id is not None:
                item['id'] = str(_id)

            for time_field in TIME_FIELDS:
                if time_field in item:
                    item[time_field] = int(item[time_field].replace(
                        tzinfo=datetime.timezone.utc).timestamp())
        except:
            pass

        return item

    async def create(self, item):
        try:
            time = datetime.datetime.utcnow()
            item['created_time'] = time
            item['updated_time'] = time

            return_item = await self.collection.insert_one(item)
            print("Return item: ", return_item)
            return_id = str(return_item.inserted_id)
            if return_id:
                item = self.convert_fields(item)
                return item
            else:
                return None
        except DuplicateKeyError as e:
            raise e
        except Exception as e:
            __logger__.error(f'create object failed: {e}')
            return None

    async def find_one_and_update(self, filter, update_body):
        try:
            item = await self.collection.find_one_and_update(
                filter,
                {
                    "$currentDate": {"updated_time": True},
                    '$set': update_body
                },
                return_document=ReturnDocument.AFTER)
            if item:
                item = self.convert_fields(item)
            return item
        except Exception as e:
            __logger__.error(f'find_and_update object failed: {e}')
            return None

    async def find_one(self, filter, exclude_fields=None):
        try:
            _id = filter.pop('_id', None) or filter.pop('id', None)
            if _id and isinstance(_id, str):
                filter['_id'] = ObjectId(_id)

            items = await self.get_list(
                filter=filter,
                size=1,
                exclude_fields=exclude_fields
            )
            print("Items find one: ", items)
            if items and len(items) > 0:
                return self.convert_fields(items[0])

            return None
        except Exception as e:
            __logger__.error(f'find object failed: {e}')
            return None

    async def get_list(
            self,
            filter,
            from_id=None,
            size=0,
            skip=0,
            order=[('_id', pymongo.DESCENDING)],
            order_type=None,
            collation=False,
            exclude_fields=[]
    ):
        try:
            conditions = filter
            if not conditions:
                conditions = {}
            exclude_filter = {}
            if exclude_fields:
                exclude_filter = dict((field, 0) for field in exclude_fields)
            if from_id:
                if order_type is None:
                    conditions["_id"] = {"$lt": ObjectId(from_id)}
                elif order_type == 1:
                    conditions["_id"] = {"$gt": ObjectId(from_id)}
                elif order_type == -1:
                    conditions["_id"] = {"$lt": ObjectId(from_id)}
            __logger__.debug(f'filter =  + {str(conditions)}')
            if collation:
                cursor = self.collection.find(filter=conditions, projection=exclude_filter, limit=size, skip=skip).sort(order) \
                    .collation({'locale': 'en'})
            else:
                cursor = self.collection.find(
                    filter=conditions, projection=exclude_filter, limit=size, skip=skip).sort(order)
            items = []
            for item in await cursor.to_list(length=100):
                item = self.convert_fields(item)
                items.append(item)
            # logger.debug(items)
            return items
        except Exception as e:
            __logger__.error(f'get_list object failed: {e}')
            return None

    async def count(self, filter):
        try:
            count = await self.collection.count(filter=filter)
            return count
        except Exception as e:
            __logger__.error(e)
            return None

    async def delete_many(self, filter):
        try:
            result = await self.collection.delete_many(filter)
            return result.deleted_count
        except Exception as e:
            __logger__.error(f'delete_many object failed: {e}')
            return None
