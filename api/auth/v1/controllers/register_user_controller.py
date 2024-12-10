from typing import Self, Protocol, Annotated

from fastapi import Depends
import schemas
from schemas import api_responses
from api.auth.v1.use_case.register_user_use_case import (
    RegiserUseCase,
    RegisterUseCaseProtocol
)

class RegisterUserControllerProtocol(Protocol):
    async def register_user(self: Self) -> api_responses.DefaultResponse:
        pass



class RegisterUserControllerImpl:
    def __init__(
            self: Self,
            RegiserUseCase: RegisterUseCaseProtocol,
    ):
        self.RegiserUseCase = RegiserUseCase


    async def register_user(self: Self) -> api_responses.DefaultResponse:
        register_data = await self.RegiserUseCase.generate_and_send_message_register()
        response_schema = api_responses.DefaultResponse(
            status_code=register_data.status_code,
            detail=register_data.detail
        )
        return response_schema


async def get_register_user_controller(
        RegiserUseCase: RegiserUseCase
) -> RegisterUserControllerImpl:
    
    return RegisterUserControllerImpl(
        RegiserUseCase=RegiserUseCase
    )


RegisterUserController = Annotated[
    RegisterUserControllerProtocol,
    Depends(get_register_user_controller)
]