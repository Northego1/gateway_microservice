import json
from typing import Self, Protocol, Annotated
import uuid

from fastapi import Depends
from api.auth.v1.gateway.custom_message import CustomMessage
from exceptions.client_exceptions import AuthError
from schemas import ms_requests, ms_responses
from api.auth.v1.gateway.message_broker_gateway import (
    MessageBrokerGateway,
    MessageBrokerProtocol
)
from logger import (
    message_logger as mes_log,
    active_id_var
)



class RefreshJwtUseCaseProtocol(Protocol):
    async def generate_and_send_message_refresh_jwt(
            self: Self,
            refresh_token: str,
            fingerprint: bytes
    ) -> ms_responses.MsReponseRefreshAccessToken:
        pass


class RefreshJwtUseCaseImpl:
    def __init__(
            self: Self,
            MessageBrokerGateway: MessageBrokerProtocol
    ) -> None:
        self.MessageBrokerGateway = MessageBrokerGateway


    async def generate_and_send_message_refresh_jwt(
            self: Self,
            refresh_token: str,
            fingerprint: bytes
    ) -> ms_responses.MsReponseRefreshAccessToken:
        try:
            active_id = str(uuid.uuid4())
            token = active_id_var.set(active_id)
            mes_log.info('Generating message to send "auth.message.consumer.refresh_jwt" route')
            payload = ms_requests.MsRequestRefreshJwt(
                refresh_token=refresh_token,
                fingerprint=fingerprint
            )
            message = CustomMessage(body=payload, correlation_id=active_id)
            headers = {'X-Processing-Function': 'refresh_jwt'}
            message.headers = headers
            mes_log.info('Message successfully generated')
            response = await self.MessageBrokerGateway.send_message(
                message=message,
                exchange_name='DIRECT',
                routing_key='auth.v1',
                reply=True
            )
            response_body_dict: dict = json.loads(response.body)
            if 400 <= response_body_dict['status_code'] < 600:
                raise AuthError(
                    status_code=response_body_dict['status_code'],
                    detail=response_body_dict['detail']
                )
            elif 200 <= response_body_dict['status_code'] < 300:
                response_schema = ms_responses.MsReponseRefreshAccessToken(
                    **response_body_dict
                )
        finally:
            active_id_var.reset(token)
        
        return response_schema
        


async def get_refresh_jwt_use_case(
        MessageBrokerGateway: MessageBrokerGateway
) -> RefreshJwtUseCaseImpl:
    return RefreshJwtUseCaseImpl(
        MessageBrokerGateway=MessageBrokerGateway
    )
    

RefreshJwtUseCase = Annotated[
    RefreshJwtUseCaseProtocol,
    Depends(get_refresh_jwt_use_case)
]