from .basemodel import MongoBaseModel
from typing import Any


class Message(MongoBaseModel):

    def __init__(self):
        super().__init__('FactoryDB', 'Message')

    _id: Any
    factory_id: str
    org_id: str 
    country: str 
    execution_date: str 
    fail_rate: float 
    defect_rate: float
