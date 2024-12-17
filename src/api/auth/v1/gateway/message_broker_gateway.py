from typing import Annotated, Optional, Protocol, Self
import uuid
from aio_pika import IncomingMessage, connect, Message, ExchangeType
from fastapi import Depends
from api.auth.v1.gateway.custom_message import CustomMessage
from producer.producer import producer
from rabbit_mq_manager import pool

from aio_pika.abc import (
    AbstractChannel,
    AbstractExchange
)
from logger import message_logger as mes_log, service_logger as serv_log


class MessageBrokerProtocol(Protocol):
    async def send_message(
        self: Self,
        exchange_name: str,
        routing_key: str,
        message: CustomMessage,
        reply: bool = True,
    ) -> Optional[IncomingMessage]:
        pass


class MessageBrokerImpl:
    async def send_message(
        self: Self,
        exchange_name: str,
        routing_key: str,
        message: CustomMessage,
        reply: bool = True,
    ) -> Optional[IncomingMessage]:
        

        # Инициализация временной очереди, если требуется ответ
        reply_queue = None
        if reply:
            channel: AbstractChannel = pool.channel_pool.get('reply_channel')
            reply_queue = await producer.get_reply_queue(
                channel=channel
            )
            message.reply_to = reply_queue.name
        try:
            await producer.send(
                message=message,
                routing_key=routing_key,
                exchange_name=exchange_name
            )
            if not reply_queue:
                return None
            
            # Ожидание ответа
            awaiting_message_id = message.correlation_id
            async with reply_queue.iterator() as queue_iter:
                mes_log.info(f'Awaiting response from {routing_key}')
                async for response in queue_iter:
                    if response.correlation_id == awaiting_message_id:
                        mes_log.info(f'Got response from {routing_key}')
                        return response

        finally:
            if reply_queue:
                await reply_queue.delete()

        return None


async def get_message_broker():
    return MessageBrokerImpl()


MessageBrokerGateway = Annotated[
    MessageBrokerProtocol,
    Depends(get_message_broker)
]