import json
from typing import Self, Protocol, Annotated
import uuid

from fastapi import Depends
from api.auth.v1.gateway.custom_message import CustomMessage
from exceptions.client_exceptions import AuthError

from api.auth.v1.gateway.message_broker_gateway import (
    MessageBrokerGateway,
    MessageBrokerProtocol
)
from schemas import (
    ms_responses,
    api_requests,
    ms_requests

)
from logger import message_logger as mes_log, active_id_var


class RegisterUseCaseProtocol(Protocol):
    async def generate_and_send_message_register(
            self: Self
    ) -> ms_responses.MsDefaultResponse:
        pass



class RegisterUseCaseImpl:
    def __init__(
            self: Self,
            MessageBrokerGateway: MessageBrokerProtocol,
            user_register_schema: api_requests.ApiRequestRegister
    ):
        self.MessageBrokerGateway = MessageBrokerGateway
        self.user_register_schema = user_register_schema


    async def generate_and_send_message_register(
            self: Self
    ) -> ms_responses.MsDefaultResponse:
        try:
            active_id = str(uuid.uuid4())
            token = active_id_var.set(active_id)
            mes_log.info('Generating message to send "auth.v1.register" route')
            payload = ms_requests.MsRequestRegister(
                username=self.user_register_schema.username,
                email=self.user_register_schema.email,
                hashed_password=self.user_register_schema.password.encode(),
            )
            message = CustomMessage(body=payload, correlation_id=active_id)
            headers = {'X-Processing-Function': 'register'}
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
                response_schema = ms_responses.MsDefaultResponse(**response_body_dict)
        finally:
            active_id_var.reset(token)
        return response_schema


async def get_register_user_controller(
        MessageBrokerGateway: MessageBrokerGateway,
        user_register_schema: api_requests.ApiRequestRegister = Depends(
            api_requests.ApiRequestRegister.as_form
        ),
) -> RegisterUseCaseImpl:
    
    return RegisterUseCaseImpl(
        MessageBrokerGateway=MessageBrokerGateway,
        user_register_schema=user_register_schema
    )


RegiserUseCase = Annotated[
    RegisterUseCaseProtocol,
    Depends(get_register_user_controller)
]