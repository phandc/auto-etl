from fastapi import Depends, Request, HTTPException
from app.endpoint.endpoint_manager import endpoint
from app.common.error import CustomException, PermissionDeniedException
from app.common.helpers.async_helper import async_wrap
from functools import wraps
from fastapi.security import OAuth2
from common.utils.constants import role_priority
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from typing import Optional
from starlette.status import HTTP_401_UNAUTHORIZED


class OAuth2PasswordWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={'tokenUrl': tokenUrl, 'scopes': scopes}
        )
        super().__init__(
            flows=flows, scheme_name=scheme_name, auto_error=auto_error
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get('token')

        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail='Not authenticated',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            return None
        return authorization


oauth2_scheme = OAuth2PasswordWithCookie(tokenUrl='')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user, _, _ = await endpoint.passport.get_user_by_token(token)
    if not user:
        raise PermissionDeniedException(
            'Signature expired. Please log in again.'
        )
    return user


def check_user_permission_with_role(require_bot_role=None, agent_position=None):
    def inner(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            if not agent_position:
                agent_id = kwargs.get('agent_id')
            else:
                agent_id = kwargs.get(agent_position).agent_id
            current_user = kwargs.get('current_user')
            agent_info = await async_wrap(endpoint.agent.get_agent_info_by_id)(agent_id)
            if not agent_info:
                raise CustomException(
                    status_code=200, message='Agent not exist', error_code=114)
            if not current_user:
                raise CustomException(
                    status_code=200, message='User not exist', error_code=40111)
            members_obj = {member['id']
                : member for member in agent_info['members']}
            if not current_user['user_id'] in members_obj:
                raise CustomException(
                    status_code=200, message='User not exist', error_code=50008)
            user_role = members_obj[current_user['user_id']]['role']
            if role_priority.get(user_role, 0) < role_priority.get(require_bot_role, 0):
                raise CustomException(
                    status_code=200, message='User dont have permission', error_code=50004)
            current_user['role'] = user_role
            return await func(*args, **kwargs)
        return wrapped
    return inner


def check_user_permission_with_role_sync_route(require_bot_role=None, agent_position=None):
    def inner(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not agent_position:
                agent_id = kwargs.get('agent_id')
            else:
                agent_id = kwargs.get(agent_position).agent_id
            current_user = kwargs.get('current_user')
            agent_info = endpoint.agent.get_agent_info_by_id(agent_id)
            if not agent_info:
                raise CustomException(
                    status_code=200, message='Agent not exist', error_code=114)
            if not current_user:
                raise CustomException(
                    status_code=200, message='User not exist', error_code=40111)
            members_obj = {member['id']
                : member for member in agent_info['members']}
            if not current_user['user_id'] in members_obj:
                raise CustomException(
                    status_code=200, message='User not exist', error_code=50008)
            user_role = members_obj[current_user['user_id']]['role']
            print(user_role)
            if role_priority.get(user_role, 0) < role_priority.get(require_bot_role, 0):
                raise CustomException(
                    status_code=200, message='User dont have permission', error_code=50004)
            current_user['role'] = user_role
            return func(*args, **kwargs)
        return wrapped
    return inner
