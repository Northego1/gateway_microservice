from typing import Self
import uuid
from fastapi import Form
from pydantic import BaseModel, ConfigDict, EmailStr, Field



class ApiRequestLogin(BaseModel):
    username: str = Field(max_length=32)
    password: str
    

    @classmethod
    def as_form(
            cls,
            username: str = Form(),
            password: str = Form()
        ) -> Self:
        return cls(username=username, password=password)
    

class ApiRequestRegister(ApiRequestLogin):
    email: EmailStr


    @classmethod
    def as_form(
            cls,
            username: str = Form(),
            password: str = Form(),
            email: EmailStr = Form()
        ) -> Self:
        return cls(username=username, password=password, email=email)