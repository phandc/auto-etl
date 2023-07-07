import logging
from typing import Optional, List
from fastapi import Query, Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from service.message import MessageService
from apis.validators.message_model import MessageResponseModel, MessagePayload
from apis.auth.authentication import api_key_auth

message_router = InferringRouter()

__logger__ = logging.getLogger(__name__)


@cbv(message_router)
class MessageAPI:

    @message_router.post('/', dependencies=[Depends(api_key_auth)])
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

    @message_router.get('/', dependencies=[Depends(api_key_auth)])
    async def get_messages(self,
                           limit: Optional[int] = Query(100, gt=0, le=1000),
                           page: Optional[int] = Query(1, gt=0),
                           sort_by: Optional[List[str]] = Query([]),
                           sort_type: Optional[int] = Query(-1),):

        data_filter = {}

        offset = (page - 1) * limit
        print(f"Limit {limit} {offset} {page} {sort_by} {sort_type}")
        result, code, msg = await MessageService().get_list_message(data_filter, limit, offset, sort_by, sort_type)
        print("result", result)
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

    @message_router.get('/{message_id}', dependencies=[Depends(api_key_auth)])
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
