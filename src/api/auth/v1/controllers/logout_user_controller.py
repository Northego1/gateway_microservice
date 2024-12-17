from typing import Self, Protocol, Annotated

from fastapi import Depends, Request

from exceptions.client_exceptions import AuthError
from utils.fingerprint_utils import extract_fingerprint_and_hash
from schemas import api_responses
from api.auth.v1 import use_case
from logger import message_logger as mes_log


class LogoutUserControllerProtocol(Protocol):
    async def logout_user(
            self: Self
    ) -> api_responses.DefaultResponse:
        pass


class LogoutUserControllerImpl:
    def __init__(
            self: Self,
            LogoutUseCase: use_case.LogoutUserUseCaseProtocol,
            fingerprint: bytes,
            request: Request
    ):
        self.fingerprint = fingerprint
        self.request = request
        self.LogoutUseCase = LogoutUseCase


    async def logout_user(
            self: Self
    ) -> api_responses.DefaultResponse:
        if not (access_token := self.request.headers.get("Authorization")):
            raise AuthError(detail='Ошибка загловоков запроса')
        refresh_token = self.request.cookies.get('refresh_jwt')
        ms_response = (
            await self.LogoutUseCase.generate_and_send_message_logout(
                refresh_token=refresh_token,
                access_token=access_token,
                fingerprint=self.fingerprint
            )
        )
        api_response = api_responses.DefaultResponse(
            status_code=ms_response.status_code,
            detail=ms_response.detail
        )
        return api_response


async def get_logout_user_controller(
        request: Request,
        LogoutUseCase: use_case.LogoutUseCase,
        fingerprint: bytes = Depends(extract_fingerprint_and_hash), 
)-> LogoutUserControllerImpl:

    return LogoutUserControllerImpl(
        request=request,
        fingerprint=fingerprint,
        LogoutUseCase=LogoutUseCase
    )  


LogoutUserController = Annotated[
    LogoutUserControllerProtocol,
    Depends(get_logout_user_controller)
]