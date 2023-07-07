from model.message import Message
import pymongo


class MessageService:

    async def create(self, payload):
        result = await Message().create(payload)
        if not result:
            return None, -1, ' Created item failed'
        
        return result, 0, 'Create items successfully'
    

    async def get_message_by_id(self, data_filter):
        result = await Message().find_one(data_filter)
        if not result:
            return None, -1, ' Get item failed'
        return result, 0, 'Get item successfully'
    

    async def get_list_message(self, filter, limit, offset, sort_by=['_id'], sort_type=-1):

        sort_order = pymongo.ASCENDING if sort_type == 1 else pymongo.DESCENDING
        sorts = []
        for sort in sort_by:
            sorts.append((sort, sort_order))
        result = await Message().get_list(filter, size=limit, skip=offset, order=sorts, order_type=sort_order)
        if not result:
            return None, -1, ' Get item failed'
        
        return result, 0, 'Get items successfully'

    async def delete_message_by_id():
        pass 

    async def update_message_by_id():
        pass
