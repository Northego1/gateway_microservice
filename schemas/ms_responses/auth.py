from pydantic import BaseModel
from enum import Enum

import schemas


class MsDefaultResponse(BaseModel):
    """Default response from microservices"""
    status_code: int
    detail: str | None


class MsLoginPayloadResponse(BaseModel):
    access_token_info: schemas.AccessTokenSchema
    refresh_token_info: schemas.RefreshTokenSchema


class MsLoginResponse(MsDefaultResponse):
    payload: MsLoginPayloadResponse | None


class MsReponseRefreshAccessToken(MsDefaultResponse):
    access_token_info: schemas.AccessTokenSchema

