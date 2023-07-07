import json
import pytest
from unittest.mock import Mock
from httpx import AsyncClient


class TestMessageAPI:
    
    @pytest.mark.asyncio
    async def test_create_message(self, db_setup=None):
        async with AsyncClient() as client:
           data = {
            "factory_id": "123xsasd2312",
            "org_id": "admvzcx21313",
            "country": "US",
            "execution_date": "2023-07-06",
            "fail_rate": 0.9,
            "defect_rate": 0.2
           }
           response = await client.post(url='http://localhost:5000/internal_api/v1/api_management/messages/', json=data)
           assert response.status_code == 200
       
    @pytest.mark.asyncio
    async def test_get_message_by_id(self, db_setup=None):
        async with AsyncClient() as client:
           response = await client.get(url='http://localhost:5000/internal_api/v1/api_management/messages/64a6eec746851c7d940b749a')
           assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_list_messages(self, db_setup=None):
        async with AsyncClient() as client:
           response = await client.get(url='http://localhost:5000/internal_api/v1/api_management/messages/?limit=5&&page=1&&sort_by=fail_rate&&sort_type=-1')
           assert response.status_code == 200
           assert len(response.json().get('data')) == 5
           assert response.json().get('data')[0]['fail_rate'] >= response.json().get('data')[1]['fail_rate']
       
       

