from typing import Optional, List 
from pydantic import BaseModel

class BaseModelArbitraryTypeAllowed(BaseModel):

    class Config:
        arbitrary_type_alllowed = True 

class BaseResponseModel(BaseModelArbitraryTypeAllowed):
    message: str 
    error_code: int = 0
    data: Optional[List]