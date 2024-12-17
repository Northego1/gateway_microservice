from typing import Optional, Union
from pydantic import BaseModel

from schemas.jwt_schemas import AccessTokenSchema




class DefaultResponse(BaseModel):
    status_code: int = 203
    detail: str | None = None
    

class ApiReponseLogin(DefaultResponse):
    access_token_info: AccessTokenSchema
    

class RefreshResponseAccess(ApiReponseLogin):
    pass



class ValidationResponseDetails(BaseModel):
    loc: list[Union[str, int]]
    msg: str
    type: str


class ValidationResponse422(BaseModel):
    status_code: int
    detail: list[ValidationResponseDetails]














