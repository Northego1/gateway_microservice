from pydantic import BaseModel, EmailStr, Field



class MsRequestLogin(BaseModel):
    username: str = Field(max_length=32)
    fingerprint: bytes
    hashed_password: bytes



class MsRequestRegister(BaseModel):
    username: str = Field(max_length=32)
    email: EmailStr
    hashed_password: bytes


class MsRequestRefreshJwt(BaseModel):
    fingerprint: bytes
    refresh_token: str


class MsRequestLogout(BaseModel):
    access_token: str
    refresh_token: str | None
    fingerprint: bytes