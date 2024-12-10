from typing import Self, Protocol, Annotated

from config import settings
from fastapi import Depends,Response
from schemas import api_responses
from api.auth.v1.use_case.login_user_use_case import (
    LoginUserUseCaseProtocol,
    LoginUserUseCase
)
from schemas import api_responses


class LoginUserControllerProtocol(Protocol):
    async def login_user(self: Self) -> api_responses.ApiReponseLogin:
        '''
        nothing to say just login controller
        '''
        pass



class LoginUserControllerImpl:
    def __init__(
            self: Self,
            response: Response,
            LoginUserUseCase: LoginUserUseCaseProtocol
    ):
        self.LoginUserUseCase = LoginUserUseCase
        self.response = response


    async def login_user(self: Self) -> api_responses.ApiReponseLogin:
        login_data = await self.LoginUserUseCase.generate_and_send_message_login()
        self.response.set_cookie(
            key='refresh_jwt',
            value=login_data.payload.refresh_token_info.token,
            httponly=True,
            max_age=settings.jwt.refresh_expire,
            samesite='strict'
        )
        response_schema = api_responses.ApiReponseLogin(
            status_code=login_data.status_code,
            detail=login_data.detail,
            access_token_info=login_data.payload.access_token_info
        )
        return response_schema




async def get_login_user_controller(
        LoginUserUseCase: LoginUserUseCase,
        response: Response
) -> LoginUserControllerImpl:
    
    return LoginUserControllerImpl(
        LoginUserUseCase=LoginUserUseCase,
        response=response
    )

LoginUserController = Annotated[
    LoginUserControllerProtocol,
    Depends(get_login_user_controller)
]