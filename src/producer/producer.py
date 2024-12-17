from typing import Optional, Self, Union
from aio_pika.abc import (
    AbstractChannel,
    AbstractExchange,
    AbstractQueue
)
from pamqp.common import Arguments
from api.auth.v1.gateway.custom_message import CustomMessage
from rabbit_mq_manager import pool
from exceptions.server_exceptions import RabbitMqError, ServerError
from logger import (
    message_logger as mes_log,
)
from logger import service_logger as serv_log



class ProducerManager:
    '''
    Единый интерфейс для управления продюсером RabbitMQ.
    В первую очередь необходимо создать канал, канал помещается 
    в словарь , где ключ - номер канала, а значение - объект класса AbstractChannel.
    Далее необходимо определить exchange, для канала, который был создан ранее.
    exchanges также хранятся в словаре, где ключ - имя exchange,
    а значение - объект класса AbstractExchange,
    после этого настройка завершена, и можно отправлять сообщения. используя 
    заранее созданый exchange
    ''' 


    async def get_reply_queue(
            self: Self,
            channel: AbstractChannel | str,
            *,
            durable: bool = False,
            exclusive: bool = True,
            auto_delete: bool = True,
            passive: bool = False,
            arguments: Arguments = None,
            timeout: Optional[Union[int, float]] = None

    ) -> AbstractQueue:
        if isinstance(channel, int):
            channel: AbstractChannel = await pool.producer_channel_pool.get(
                name=channel
            )
        try:
            serv_log.debug(f'Trying to create reply queue')
            queue = await channel.declare_queue(
                durable=durable,
                passive=passive,
                exclusive=exclusive,
                auto_delete=auto_delete,
                arguments=arguments,
                timeout=timeout
            )
            serv_log.debug(f'Reply queue  successfully created')
            return queue
        except Exception:
            serv_log.error(f'Creating reply queue is failed')


    async def send(
            self: Self,
            message: CustomMessage,
            exchange_name: str,
            routing_key: str | None = None,
            *,
            mandatory: bool = True,
            immediate: bool = False,
            timeout: Optional[Union[int, float]] = None
    ):
        '''
        Обертка для отправки сообщения, нужно передать имя
        уже зарегестрированного exchange_name и message
        '''
        exchange = pool.exchange_pool.get(exchange_name)
        try:
            mes_log.info(f'Trying to send message to {routing_key} ')
            await exchange.publish(
                message=message,
                routing_key=routing_key,
                mandatory=mandatory,
                immediate=immediate,
                timeout=timeout
            )
            mes_log.info(f'Message by exchange successfully sent to {routing_key}')
        except Exception as e:
            mes_log.error(f'Sending message by exchange is failed')
            raise RabbitMqError()

    
producer = ProducerManager()