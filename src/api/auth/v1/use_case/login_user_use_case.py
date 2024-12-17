import json
from typing import Self, Protocol, Annotated
import uuid

from fastapi import Depends
from api.auth.v1.gateway.custom_message import CustomMessage

from schemas import api_requests
from schemas import ms_responses

from schemas import ms_requests
from api.auth.v1.gateway.message_broker_gateway import (
    MessageBrokerGateway,
    MessageBrokerProtocol
)
from exceptions.client_exceptions import AuthError
from logger import message_logger as mes_log, active_id_var
from utils.fingerprint_utils import extract_fingerprint_and_hash



class LoginUserUseCaseProtocol(Protocol):
    async def generate_and_send_message_login(
            self: Self
    ) -> ms_responses.MsLoginResponse:
        '''
        nothing to say just login controller
        '''
        pass



class LoginUserUseCaseImpl:
    def __init__(
            self: Self,
            MessageBrokerGateway: MessageBrokerProtocol,
            user_login_schema: api_requests.ApiRequestLogin,
            fingerprint: bytes
    ):
        self.MessageBrokerGateway = MessageBrokerGateway
        self.user_login_schema = user_login_schema
        self.fingerprint = fingerprint


    async def generate_and_send_message_login(
            self: Self
    ) -> ms_responses.MsLoginResponse:
        try:
            active_id = str(uuid.uuid4())
            token = active_id_var.set(active_id)
            mes_log.info('Generating message to send "auth.message.consumer.login" route')
            payload = ms_requests.MsRequestLogin(
                username=self.user_login_schema.username,
                hashed_password=self.user_login_schema.password.encode(),
                fingerprint=self.fingerprint
            )
            message = CustomMessage(body=payload, correlation_id=active_id)
            headers = {'X-Processing-Function': 'login'}
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
                response_schema = ms_responses.MsLoginResponse(
                    **response_body_dict
                )
        finally:
            active_id_var.reset(token)
        return response_schema


async def get_login_user_controller(
        MessageBrokerGateway: MessageBrokerGateway,
        user_login_schema: api_requests.ApiRequestLogin = Depends(
            api_requests.ApiRequestLogin.as_form
        ),
        fingerprint: bytes = Depends(extract_fingerprint_and_hash)
) -> LoginUserUseCaseImpl:
    
    return LoginUserUseCaseImpl(
        MessageBrokerGateway=MessageBrokerGateway,
        user_login_schema=user_login_schema,
        fingerprint=fingerprint
    )


LoginUserUseCase = Annotated[
    LoginUserUseCaseProtocol,
    Depends(get_login_user_controller)
]