from typing import Optional, List, Any
from apis.validators.base_validators import BaseResponseModel, BaseModelArbitraryTypeAllowed


class MessageResponseModel(BaseModelArbitraryTypeAllowed):
    id: Any 
    factory_id: str
    org_id: str 
    country: str 
    execution_date: str #convert to utc timestamp
    fail_rate: float 
    defect_rate: float

class MessagePayload(BaseModelArbitraryTypeAllowed):
    factory_id: str
    org_id: str 
    country: str 
    execution_date: str #convert to utc timestamp
    fail_rate: float 
    defect_rate: float
    

