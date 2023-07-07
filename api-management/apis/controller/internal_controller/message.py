import logging
from typing import Optional, List
from fastapi import Query
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from service.message import MessageService
from apis.validators.message_model import MessageResponseModel, MessagePayload


internal_message_router = InferringRouter()

__logger__ = logging.getLogger(__name__)


@cbv(internal_message_router)
# todo: co cho filter theo factory_id ko
class InternalMessageAPI:

    @internal_message_router.post('/')
    async def create_message(self, payload: MessagePayload):
        data = payload.dict()
        result, code, msg = await MessageService().create(data)
        print("result", result)
        if not result:
            return {
                'error_code': code,
                'message': msg
            }
        result = MessageResponseModel(**result)
        return {
            'data': result,
            'error_code': code,
            'message': msg
        }

    @internal_message_router.get('/')
    async def get_messages(self,
                           limit: Optional[int] = Query(100, gt=0, le=1000),
                           page: Optional[int] = Query(1, gt=0),
                           sort_by: Optional[List[str]] = Query([]),
                           sort_type: Optional[int] = Query(-1),):

        data_filter = {}
        offset = (page - 1) * limit
        result, code, msg = await MessageService().get_list_message(data_filter, limit, offset, sort_by, sort_type)
        if not result:
            return {
                'error_code': code,
                'message': msg
            }
        return {
            'data': result,
            'error_code': code,
            'message': msg
        }

    @internal_message_router.get('/{message_id}')
    async def get_message_id(self, message_id: str):
        if not message_id:
            return {
                'error_code': -1,
                'message': 'Invalid message id'
            }
        data_filter = {
            '_id': message_id
        }
        result, code, msg = await MessageService().get_message_by_id(data_filter)

        if not result:
            return {
                'error_code': code,
                'message': msg
            }
        result = MessageResponseModel(**result)
        return {
            'data': result,
            'error_code': code,
            'message': msg
        }
