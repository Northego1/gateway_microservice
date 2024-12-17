from typing import Self, Protocol, Annotated

from fastapi import Depends, Request
from exceptions.client_exceptions import AuthError
from schemas import api_responses
from api.auth.v1 import use_case
from utils.fingerprint_utils import extract_fingerprint_and_hash



class RefreshJwtControllerProtocol(Protocol):
    async def refresh_access_token(
            self: Self
    ) -> api_responses.RefreshResponseAccess:
        '''
        Обновляет токен доступа, в случае различия текущего фингерпринта
        от фингерпринта записанного для этого рефреш токена в базе данных,
        деактивирует рефреш токен, путем удаления соотвестующей записи из базы 
        данных и возвращает ошибку клиента 403
        '''



class RefreshJwtControllerImpl:
    def __init__(
            self: Self,
            RefreshJwtUseCase: use_case.RefreshJwtUseCaseProtocol,
            fingerprint: bytes,
            request: Request
    ) -> None:
        self.RefreshJwtUseCase = RefreshJwtUseCase
        self.fingerprint = fingerprint
        self.request = request

    async def refresh_access_token(
            self: Self,
            
    ) -> api_responses.RefreshResponseAccess:
        if not (refresh_token := self.request.cookies.get('refresh_jwt')):
            raise AuthError(detail='Отсутствует refresh token')
        ms_response = (
            await self.RefreshJwtUseCase.generate_and_send_message_refresh_jwt(
                refresh_token=refresh_token,
                fingerprint=self.fingerprint
            )
        )
        api_response = api_responses.RefreshResponseAccess(
            status_code=ms_response.status_code,
            detail=ms_response.detail,
            access_token_info=ms_response.access_token_info
        )
        return api_response


async def get_refresh_jwt_controller(
        RefreshJwtUseCase: use_case.RefreshJwtUseCase,
        request: Request,
        fingerprint: bytes = Depends(extract_fingerprint_and_hash),  
) -> RefreshJwtControllerImpl:
    
    return RefreshJwtControllerImpl(
        RefreshJwtUseCase=RefreshJwtUseCase,
        fingerprint=fingerprint,
        request=request
    )
    

RefreshTokenController = Annotated[
    RefreshJwtControllerProtocol,
    Depends(get_refresh_jwt_controller)
]